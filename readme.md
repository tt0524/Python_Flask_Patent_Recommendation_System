# CMPE 256 2019 Summer Group Project

In this project, we implement a patent recommendation system combining search and recommendation functions.
You may view the report, app source code and demo video here.

# TEAM 7 - Patent Recommendation System

Team Members:
* Aaron Lee (ID: 009085596)
* Hongfei Xu (ID:011833978)
* Juan Chen (ID: 012483250)
* Xiaoting Jin (ID: 013842192)

# Contents

* [Final Report](https://github.com/256xu/CMPE256Team7/blob/master/CMPE%20256%20Project%20Report.pdf)
* [Demo and Presentation Video](https://youtu.be/c1Gmq4IN48c)
* [Web Application Source Codes](https://github.com/256xu/CMPE256Team7/tree/master/app_patent_recommend_master)


* [Jupyter Notebook Codes and Data](https://github.com/256xu/CMPE256Team7/tree/master/jupyter_codes_and_data)
* [Middle & Final Slides](https://github.com/256xu/CMPE256Team7/tree/master/project_slides)


# Running App Locally
## Dependencies
* Python 3.7
* flask
* sqlite
* pandas

1. Download [whole package and enter in folder ”app_patent_recommend_master“](https://github.com/256xu/CMPE256Team7)
2. Install packages by

`pip install -r requirements.txt`

3. Download the common stopwords by

`python recommender/download.py`

then select to download the `popular` section.

4. Set the env variable

`sudo ./setenv.sh`

5. Initialize the sqlite db by

`python manage.py initdb`

6. Start the app by

`python manage.py runserver`


**If you have two versions of python locally(eg. python2.7 and python3.7), please modify the commands above from** `python` **and** `pip` **to** `python3` **and** `pip3` .

7. After running commands above, wait for a few minutes, when you see: 

  `* Debugger is active!`
  
  `* Debugger PIN: 406-***-***`
  
  
   which means app activates sucessfully, then you can try our app at http://127.0.0.1:5000/  (currently unavailable)


