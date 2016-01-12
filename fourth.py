from flask import Flask, render_template, request, jsonify
from app import app
from flask import Response, stream_with_context
import twitter, json
from app import views, db, models
import datetime
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from app import forms
#from datetime import datetime
from apscheduler.scheduler import Scheduler
import time
import logging
import pytz
import codecs
#from datetime import datetime
import sys
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
from sqlalchemy import func
import csv , codecs
from embedly import Embedly
from instagram.client import InstagramAPI
try:
    # python 3
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
except:
    # python 2
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

reload(sys)  
sys.setdefaultencoding('utf-8')

# app = Flask(__name__)  // i don't know what the fuck this means
sched = Scheduler()
# meta = {'title':'', 'heading':''}

def auth():
	CONSUMER_KEY = 'I47BdneAhfRdY9Bydvew'
	CONSUMER_SECRET = 'griaF4nTCcC6Y1DDzx3VCdpnn5cgUJSYOtThriGTY'
	ACCESS_TOKEN_KEY = '121376048-8gixtBQQX9fJmnGtGgmtKZvfHgIUGR3gy3pGIYf9'
	ACCESS_TOKEN_SECRET = 'NeGrue52HdgbIZ6cb3ePakHOtFL0DZyJkpLgA2el3AW5j'
	api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

   	return api

def check_woe(country_code):	
	country_code = country_code.upper()
	#add this to config file, 
	WOE_ID = {		
		'GLOBAL':1, 
		'PH':23424934,
		'US':23424977
	}
	
	if country_code in WOE_ID:
		result = WOE_ID[country_code] 
	else:
		result = False 
	
	return result

def twitter_auth():
	#checking import twitter
	#add this to config file
	CONSUMER_KEY = 'd7tKl4qajMQmpwjIbPw'
	CONSUMER_SECRET ='v5Utf5ewYrKdLe7VIHiNLBiPehSdG5gDoqEbPfHRB8A'
	OAUTH_TOKEN = '126343897-sT0c0Fpt6qzrd91TiBbGlPWS3Uov9Z1yhtG6c2on'
	OAUTH_TOKEN_SECRET = 'uFe1tYjoxX5Tf0o5NjHo0wKxTyzvGEPL3GmoRp0LlCDkD'
	#add this to config file

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

@app.route('/track/<path:key>')
def lol(key):
	api = auth()
	for item in api.request('statuses/filter', {'track': key}):
    	   	res = item['text'] if 'text' in item else item
    	   	retweet = item['retweet_count'] if 'text' in item else item
    	   	favorites = item['favorite_count'] if 'text' in item else item
    	   	name = item['user']['screen_name'] if 'text' in item else item
    	   	real = item['user']['name'] if 'text' in item else item
    	   	pic = item['user']['profile_image_url_https'] if 'text' in item else item
    	   	followers = item['user']['followers_count'] if 'text' in item else item
    	   	date = item['created_at'] if 'text' in item else item
    	   	lol = ''
    	   	filtered = name.find('Smart') == -1 and res.find('abs') == -1 and res.find('pinasmile') == -1 and res.find('cbn') == -1
    	   	if not filtered:
    	   		continue
    	   	if 'media' in item['entities']:
    	   		for image in item['entities']['media']:
    	   			image = client.oembed(image['media_url'])
    	   			lol = image['url']
    	   	elif 'urls' in item['entities']:
    	   		for url in item['entities']['urls']:
    	   			url = client.oembed(url['url'])
    	   			lol = url['url']
    	   	else:
    	   		lol = ''
    	   	print res
    	   	print date

    		t = models.Trace(tweet=key, key=res, retweet=retweet, favorites=favorites, name=name, real=real, pic=pic, followers=followers, date=date,embed=lol)
    		db.session.add(t)
    		db.session.commit()
    		lol = None
    	return render_template('get.html', result='Tracing is now initiliaze!')
    	
@app.route('/instagram/<path:key>')
def instagram(key):
	api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
	for item in api.media_search(q=key, count=10, lng=120.98, lat=14.62):
		key = key
		photo = item.images['low_resolution'].url
		username = item.user.username
		real_name = item.user.full_name	
		dp = item.user.profile_picture
		date = item.created_time
		print date, photo , real_name	
	lol = "text"
	return lol
@app.route('/instagram/users/<path:key>')
def instagram1(key):
	api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
	for item in api.user_search(q=key, count=10):
		username = item.username
		dp = item.profile_picture
		did = item.id
		web = item.website

		bio = item.bio
		print dp, username, did,web, bio
	lol = "text"
	return lol
@app.route('/instagram/media/<path:key>')
def instagram2(key):
	api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
	for item in api.user_recent_media(user_id=key, count=20, max_id=100):
		photo = item.images
		print dp, username, did,web, bio
	lol = "text"
	return lol
@app.route('/tag_search')
def tag_search():
    api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
    tag_search, next_tag = api.tag_search(q="thefuturepark")
    tag_recent_media, next = api.tag_recent_media(user_id="userid", tag_name=tag_search[0].name)
    photos = []
    content = "<h2>Media Search</h2>"
    for tag_media in tag_recent_media:
        # print tag_media
        res = tag_media.caption.text
        retweet = 0
        favorites = tag_media.like_count
        name = tag_media.user.username
        real = tag_media.user.full_name
        pic = tag_media.user.profile_picture
        followers = 0
        # date = unicode(tag_media.created_time.replace(microsecond=0))
        date = tag_media.created_time
        print date
        embed = tag_media.get_standard_resolution_url()
        enable = True
        photos.append('<img src="%s"/>' % tag_media.get_standard_resolution_url())
    	photos.append(tag_media.caption.text)
    	data = models.Trace.query.filter(models.Trace.key==res)
    	if data.count() > 0:
    		print "kaparehas"
    	else:
    		print "wala"
    		t = models.Trace(tweet='thefuturepark', key=res, retweet=retweet, favorites=favorites, name=name, real=real, pic=pic, followers=followers, date=date,embed=embed,enable=enable)
    		db.session.add(t)
    		db.session.commit()
    content += ''.join(photos)
    	
    return content

@app.route('/insta/<path:key>')
def subscribe(key):
	api = InstagramAPI(client_id='14c7fb94b134473d9ee9cc449face034', client_secret='1738e7489ef24de0abef9a0dbfa8d3ea')
	api.create_subscription(object='tag', object_id=key, aspect='media', callback_url='http://127.0.0.1:3001/insta/thefuturepark')
	for item in api.user_recent_media(user_id=key, count=20, max_id=100):
		photo = item.images
		print dp, username, did,web, bio
	lol = "text"
	return lol

sched.start()
print "end of line"
logging.basicConfig()


if __name__ == '__main__':
    app.run(debug=True,port=3001)	

