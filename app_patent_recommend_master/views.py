from flask import render_template, request, redirect, url_for, flash, make_response
import common
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager, current_user
from login_form import LoginForm
from models import User, ClickHistory
import util
from application import app, db
from recommender import hybrid_pipeline
from recommender import user_based
from recommender import content_based_revised
from recommender import item_based

# use login manager to manage session
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app=app)


# The callback to reload User object.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)

        print(user_name, password)

        user = User(user_name, password)
        temp_users = User.query.filter_by(username=user_name).all()
        if not (temp_users and len(temp_users) > 0):
            error = "username does not exist!"
            return render_template('login.html', title="Log In", error=error)

        if password == temp_users[0].password:
            login_user(user)
            flash("{0} were successfully logged in.".format(current_user.username))
            return redirect(url_for('homepage', title="{0}".format(user.username)))
        else:
            error = "username and password do not match!"
            return render_template('login.html', title="Log In", error=error)
    return render_template('login.html', title="Log In")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Register Your Account')

    inputs = util.request_form_to_json(request)
    if inputs['password'] != "" and inputs['username'] != "":
        user = User(inputs['username'], inputs['password'])
        print(user)
        existed_users = User.query.filter_by(username=inputs['username']).all()
        if len(existed_users) > 0:
            message = "{} already existed in db.".format(inputs['username'])
            flash("{} already existed in db.".format(inputs['username']))
            return render_template('register.html', warning=message)
        try:
            db.session.add(user)
            db.session.commit()
            flash("{0} saved successfully.".format(user.username))
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return render_template('register.html', warning=str(e))
    else:
        warning = "Username and password is empty"
        return render_template('register.html', title="Get Code", warning=warning)


@app.route('/logout')
@login_required
def logout():
    print("{0} is authenticated {1}".format(current_user, current_user.is_authenticated))
    username = get_current_username()
    logout_user()
    message = "{0} is authenticated {1}".format(current_user, current_user.is_authenticated)
    print(message)
    flash("{0} has been logged out. ".format(username))
    return redirect(url_for('login'))


@app.route("/")
def homepage():
    print("current user {0} ".format(current_user))
    return render_template('search.html', username=get_current_username())


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        inputs = _get_form_fields()
        print({"inputs": inputs})
        result = hybrid_pipeline.hybrid_pipe(
            patent_id=None,
            after=inputs[common.AFTER],
            before=inputs[common.BEFORE],
            kind=inputs[common.KIND],
            cpc=inputs[common.CPC],
            inventor=inputs[common.INVENTOR],
            lawyer=inputs[common.LAWYER],
            assignee=inputs[common.ASSIGNEE],
            sentence=inputs[common.KEYWORDS])
        result['id'] = result['id'].astype(int)
        result = result.values.tolist()[:10]
        print("\n hybrid result {0}\n\n".format(result))
        headline = "Top recommended patents based on hybrid recommendation"
        return render_template('search.html', items=result, CPC_VALUES=common.CPC_VALUES,
                               page_headline=headline,
                               username=get_current_username)
    else:
        return redirect(url_for('homepage'))


@app.route('/more', methods=['POST'])
@login_required
def save_clicked_items():
    username = get_current_username()
    if 'clicked_items' in request.cookies:
        items_in_string = request.cookies['clicked_items']
        clicked_items = get_distinct_items(items_in_string, '%2C')
        print(clicked_items)
        print("current user {0}".format(current_user))

        clicks = ClickHistory.query.filter_by(username=username).all()
        history_patent_ids = {click.patent_id for click in clicks}
        print("clickes type: {0} value: {1}".format(type(clicks), clicks))

        for patent_id in clicked_items:
            if patent_id not in history_patent_ids:
                click = ClickHistory(current_user.username, patent_id)
                db.session.add(click)
                db.session.commit()

    history = get_user_click_history()
    print(history)
    print("===============\n")

    result = user_based.search_similar_user(username, history)
    print("User Based Click History result: {0}".format(result))
    if not result.empty:
        result = result.values.tolist()
    else:
        result = []
    print("type of result {0} with value {1}".format(type(result), result ))
    headline = "Refined recommendations based on {0}'s click history.".format(get_current_username())

    response = make_response(render_template('search.html',
                                             items=result ,
                                             CPC_VALUES=common.CPC_VALUES,
                                             username=get_current_username(),
                                             page_headline=headline
                                             ))
    response.delete_cookie('clicked_items', path='/')
    return response

@app.route('/similar', methods=['GET'])
def recommend_similar_patents():
    patent_id = request.args.get('patent_id')
    if patent_id:
        result = content_based_revised.tfidf_similarity(int(float(patent_id)))
        result['id'] = result['id'].astype(int)
        print("Content Based Recom: {0}".format(result))
        if len(result) > 0:
            result = result.values.tolist()
        page_headline = "Similar patents for patent id {0} based on Content(TF_IDF) ".format(patent_id)
        return render_template('search.html', items=result,
                               CPC_VALUES=common.CPC_VALUES,
                               username=get_current_username(),
                               page_headline=page_headline)
    return redirect(url_for('homepage'))


@app.route('/citation', methods=['GET'])
def recommend_related_items_based_on_citations():
    patent_id = request.args.get('patent_id')
    if patent_id:
        result = item_based.search_similar_item_citation(patent_id)
        print("\n\n item based result: type {0} value {1}".format(type(result), result))
        if not result.empty:
            result = result.values.tolist()
        else:
            result = []
        page_headline = "Related patents for patent_id {0} (Item based Collaborative Filtering) ".format(patent_id)
        return render_template('search.html', items=result,
                               CPC_VALUES=common.CPC_VALUES,
                               username=get_current_username(),
                               page_headline=page_headline)
    return redirect(url_for('homepage'))


def _get_form_fields():
    inputs = {}
    for key in common.SEARCH_FORM_FIELDS:
        if request.form.get(key):
            inputs[key] = request.form.get(key)
        else:
            inputs[key] = None
    return inputs


def _refined_recommend_items(username, clicked_items):
    result = list()
    for i in range(len(clicked_items)):
        result.append({})
    return result


def get_distinct_items(items_in_string, delimiter):
    items = items_in_string.split(delimiter)[:-1]
    return list(set(items))


def get_user_click_history():
    all_users = User.query.all()
    click_history = dict()
    if all_users:
        for user in all_users:
            username = user.username
            clicks = ClickHistory.query.filter_by(username=username).all()
            patent_ids = {click.patent_id for click in clicks if clicks}
            if len(patent_ids) > 0:
                click_history[username] = patent_ids
    return click_history


def get_current_username():
    return current_user.username if current_user.is_authenticated else None
