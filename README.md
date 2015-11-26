# **Social Media Listener for Twitter using Python**
## Table of Contents

* [Team Members](#team-members)
* [Synopsis](#synopsis)
* [Installation](#install)
 
##<a name="team-members"></a>**Team Members**
* "John Frederick Marquez" <loloy@bitbucket.org>
* "Julian Austin Macmang" <julianmacmang@bitbucket.org>
* "Jofell Galardo" <jgallardo@bitbucket.org>

##**Synopsis**<a id="synopsis"></a> 
	This python program is use to harvest trending topics, to stream tweets by keyword and to take the sentiments of the user. This program is still on process so there will be some changes by time goes by.

##<a id="install"></a>**Installation**
	* Install python 2.7
	* Pull the Repository
	* Download [virtualenv.py](https://raw.githubusercontent.com/pypa/virtualenv/1.9.X/virtualenv.py) and put it inside the folder.
	* Create the virtual environment by entering this command:
		python virtualenv.py <name of folder>
	* Activate the virtual environment by entering this command:
		. flask/bin/activate
	* Install all neccessary requirements:
		pip install flask==0.9
		pip install flask-login
		pip install flask-openid
		pip install flask-mail==0.7.6
		pip install sqlalchemy==0.7.9
		pip install flask-sqlalchemy==0.16
		pip install sqlalchemy-migrate==0.7.2
		pip install flask-whooshalchemy==0.55a
		pip install flask-wtf==0.8.4
		pip install pytz==2013b
		pip install flask-babel==0.8
		pip install flup
		pip install twitter
		pip install apscheduler
		pip install twitterapi
	* Create a database file by running the script:
		python db_create.py
	* Migrate the database using:
		python db_migrate.py
	* Then you are ready to go:
		python run.py 
