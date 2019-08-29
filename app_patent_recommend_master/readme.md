# Patent Recommender 

Recommendation system powered by recommendation models.
## Implemented by Team #7
* Aaron Lee (ID: 009085596)
* Hongfei Xu (ID:011833978)
* Juan Chen (ID: 012483250)
* Xiaoting Jin (ID: 013842192)

# Dependencies
* Python 3.7
* flask
* sqlite
* pandas


1. Download [Web Application Source Codes](https://github.com/256xu/CMPE256Team7/tree/master/app_patent_recommend_master)
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
  
    which means app activates sucessfully, then you can try our app at http://127.0.0.1:5000/ 




# LINKs
YouTube: https://youtu.be/c1Gmq4IN48c

Repository Homepage: https://github.com/256xu/CMPE256Team7
