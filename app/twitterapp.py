from flask.ext.admin import Admin
from flask import Flask, render_template, request, jsonify
from app import app
from flask import Response, stream_with_context
import twitter, json
from app import views, db, models
import datetime
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import forms
#from datetime import datetime
from apscheduler.scheduler import Scheduler
import time
import logging
import pytz
import codecs
from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth
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


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '1501311503425518'
FACEBOOK_APP_SECRET = 'dfdf0554845a64973e0e99f9c2be6d89'
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')



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

@app.route('/home')
@app.route('/trends/show')
def show_trends():	
	meta={}
	meta['heading'] = 'Global Trends'
	meta['title'] = 'Trending List'
	
	trends = models.Trends.query.order_by(models.Trends.timestamp.desc())
	# xxx = models.Trends.get_trends()
	# import sys
	# sys.exit(trends)
	# for t in trends:
		# for k, v in vars(t).iteritems():
			# print k
	# keyValues = list(trends.items())
	# for t in trends:
		# for key, value in trends.items():
			# print key, value
		# print t.keyword, t.woe_id, t.woe_code, t.timestamp
	# return t

	return render_template('results.html', meta=meta, result=trends)


@app.route('/trends/show/<path:country_code>')
def show_trends_country(country_code):
	country_exists = check_woe(country_code)
	meta = {}
	meta['heading'] = 'Trending keywords in '+country_code.upper()
	meta['title'] = 'Trending List'
	if country_exists != False:
		trends = models.Trends.query.filter_by(woe_id = country_exists).order_by(models.Trends.timestamp.desc())
		result = trends
		# for t in trends:
			# print t.keyword	
	else:
		result['message'] = 'No Result for this'
		#result['title'], result['header'], result['trends']
		# for t in trends:
		# print t.keyword, t.woe_id, t.woe_code, t.timestamp
	
	return render_template('results.html', result=result, meta=meta)

 
@app.route('/trends/get/<path:country_code>') 
def get_trending_keywords(country_code):
	sched.add_cron_job(get_trend,args=[country_code], minute='*/30')
	return get_trend(country_code)
	

#@sched.interval_schedule(seconds=5)
def get_trend(country_code):

	country_id = check_woe(country_code)
	if country_id:
		#start twitter authenticate
		twitter_api = twitter_auth()
		trends_results = twitter_api.trends.place(_id=country_id)
				
		trendlist = []

		if trends_results:

			for child in trends_results:

				if child['locations']:
					for sub in child['locations']:
						country_code = sub['woeid']
						country_name = sub['name']

				if child['trends']:
		    			for subchild in child['trends']:
		        			
		        			if subchild['name']:
		        				trendlist.append(subchild['name'])
		        				# print subchild['name'].encode('utf-8')+subchild['query'].encode('utf-8')+subchild['name'].encode('utf-8')
						t = models.Trends(keyword=subchild['name'], woe_id=country_code, woe_code=country_name, timestamp = datetime.datetime.now(tz=pytz.utc) )

						db.session.add(t)
						db.session.commit()
			result = trendlist
			# result = 'Got trending keywords from Twitter  in  %s' % country_name;		
	else:
		result =  'This feature is not available for this country'

	return render_template('get.html', result=result)	

@app.route('/search', methods=['GET','POST'])
def search():
	form = forms.SearchForm(request.form)
	result = ''
	debug =''
	message=''	

	if request.method == 'POST' and form.validate():
		q = request.form["searchKeyword"]
		geocode = [14.083333333333334,120.96666666666667,100]
		twitter_api = twitter_auth()
		count = 200
		#	lang = 'us' #tl
		result_type = 'popular'
		# until ='2014-11-12'
		search_results = twitter_api.search.tweets( q=q, count=count)
		statuses = search_results['statuses']
		message = str(len(statuses))+' results for \''+q+'\''
		result = statuses
		for item in result:
			res = item['text'] if 'text' in item else item
			print res
			retweet = item['retweet_count'] if 'text' in item else item
			print retweet
			favorites = item['favorite_count'] if 'text' in item else item
			print favorites
			name = item['user']['screen_name'] if 'text' in item else item
			print name
			real = item['user']['name'] if 'text' in item else item
			print real
			pic = item['user']['profile_image_url_https'] if 'text' in item else item
			print pic
			followers = item['user']['followers_count'] if 'text' in item else item
			print followers
			date = item['created_at'] if 'text' in item else item
			print res,date
			if 'media' in item['entities']:
				for image in item['entities']['media']:
					image = image['media_url']
			else:
				image = ''
			print image
			t = models.Search(tweet=q, key=res, retweet=retweet, favorites=favorites, name=name, real=real, pic=pic, followers=followers, date=date, embed = image)
			db.session.add(t)
			db.session.commit()
		# print result
		# for _ in range(5):
		# 	# print "Length of statuses", len(statuses)
		# 	try:
		# 		 next_results = search_results['search_metadata']['next_results']
		# 	except KeyError, e: # No more results when next_results doesn't exist
		# 		 break

		# 	kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
		# 	print kwargs	    
	 #    	result = search_results = twitter_api.search.tweets(**kwargs)
	 #    	statuses += search_results['statuses']
	 #    	result = statuses
	return render_template('search.html', message=message, result=result, form=form, debug=debug)
@app.route('/search/lol', methods=['GET','POST'])
def wew():
	form = forms.SearchTrace(request.form)
	trends = ''
	if request.method == 'POST' and form.validate():
		key = request.form["searchTrace"]
		trends = models.Search.query.filter_by(tweet=key).order_by(models.Search.id.desc())
		print trends
	else:
		trends = models.Search.query.order_by(models.Search.id.desc())
	return render_template('trace.html', result=trends, form=form)
key = '29fd40eda47344aa93268b96a3e86879'
client = Embedly(key)
@app.route('/track/<path:key>',methods=['GET','POST'])
def filtering(key):
	form = forms.Trace(request.form)
	filters = None
	if request.method == 'POST':
		filters = request.form["filterText"]
		if filters == '':
			return no(key)
		else:
			arral = filters.split('\r\n')
			print arral
			return lol(key,arral)
	else:
		print "Error"
		return render_template('filter.html', result=filters, form=form)
def no(key):
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
    	   	enable = True
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
    		t = models.Trace(tweet=key, key=res, retweet=retweet, favorites=favorites, name=name, real=real, pic=pic, followers=followers, date=date,embed=lol,enable=enable)
    		db.session.add(t)
    		db.session.commit()
    		lol = None
    	return render_template('get.html', result='Tracing is now initiliaze!')



def lol(key,arral):
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
    	   	filtered = True
    	   	for fil in arral:
    	   		filtered = filtered and res.find(fil.lower()) == -1 and res.find(fil.upper()) == -1 and name.find(fil.lower()) == -1 and name.find(fil.upper()) == -1
    	   	print fil
    	   	print filtered
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
    	   	enable = True
    		t = models.Trace(tweet=key, key=res, retweet=retweet, favorites=favorites, name=name, real=real, pic=pic, followers=followers, date=date,embed=lol,enable=enable)
    		db.session.add(t)
    		db.session.commit()
    		lol = None
    	return render_template('get.html', result='Tracing is now initiliaze!')
    	
@app.route('/track/show', methods=['GET','POST'])
def show():
	form = forms.SearchTrace(request.form)
	trends = ''
	if request.method == 'POST' and form.validate():
		key = request.form["searchTrace"]
		trends = models.Trace.query.filter_by(tweet=key).order_by(models.Trace.id.desc())
		print trends
	else:
		trends = models.Trace.query.order_by(models.Trace.id.desc())
	return render_template('trace.html', result=trends, form=form)

#returns data in json by id number

@app.route('/track/show/tweets/<path:id>')
def get_tracker(id):
		cols = ['id', 'key', 'tweet', 'retweet', 'favorites', 'name', 'real','pic','followers','date','embed']
		data = models.Trace.query.filter_by(id=id)
		result = [{col: getattr(d, col) for col in cols} for d in data]
		return jsonify(results=result)


#returns data in json by id number search 
@app.route('/search/show/tweets/<path:id>')
def get_track(id):
		cols = ['id', 'key', 'tweet', 'retweet', 'favorites', 'name', 'real','followers','date','embed']
		data = models.Search.query.filter_by(id=id)
		result = [{col: getattr(d, col) for col in cols} for d in data]
		return jsonify(results=result)


#return all data in json & csv
@app.route('/track/show/tweets')
def get_loll():
		cols = ['id', 'key', 'tweet', 'retweet', 'favorites', 'name', 'real','pic','followers','date','embed']
		data = models.Trace.query.order_by(models.Trace.id.desc())
		result = [{col: getattr(d, col) for col in cols} for d in data]
		out = csv.writer(codecs.open('tweet.csv','w'), delimiter=',',quoting=csv.QUOTE_ALL)
		out.writerow(["id","tweet_text","date_created","twitter_name","real_name","profile_pic","embedded_pic"])
		for d in data:
			did = d.id
			dkey = d.key.encode('utf-8')
			ddate = d.date.encode('utf-8')
			dtwitter = d.name.encode('utf-8')
			dname = d.real.encode('utf-8')
			dpic = d.pic.encode('utf-8')
			dembed = d.embed.encode('utf-8')
			results = [did, dkey, ddate, dtwitter,dname,dpic,dembed]			
			out.writerow(results)
		return jsonify(results=result)

#return all data in json & csv search
@app.route('/search/show/tweets')
def get_lol():
		cols = ['id', 'key', 'tweet', 'retweet', 'favorites', 'name', 'real','pic','followers','date','embed']
		data = models.Search.query.all()
		result = [{col: getattr(d, col) for col in cols} for d in data]
		out = csv.writer(codecs.open('search.csv','w'), delimiter=',',quoting=csv.QUOTE_ALL)
		out.writerow(["id","tweet_text","date_created","twitter_name","real_name","profile_pic","embedded_pic"])
		for d in data:
			did = d.id
			dkey = d.key.encode('utf-8')
			ddate = d.date.encode('utf-8')
			dtwitter = d.name.encode('utf-8')
			dname = d.real.encode('utf-8')
			dpic = d.pic.encode('utf-8')
			dembed = d.embed.encode('utf-8')
			results = [did, dkey, ddate, dtwitter,dname,dpic,dembed]			
			out.writerow(results)
		return jsonify(results=result)










# @app.route('/instagram/<path:key>')
# def instagram(key):
# 	api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
# 	for item in api.media_search(q=key, count=10, lng=120.98, lat=14.62):
# 		key = key
# 		photo = item.images['low_resolution'].url
# 		username = item.user.username
# 		real_name = item.user.full_name	
# 		dp = item.user.profile_picture
# 		date = item.created_time
# 		print date, photo , real_name	
# 	lol = "text"
# 	return lol
# @app.route('/instagram/users/<path:key>')
# def instagram(key):
# 	api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
# 	for item in api.user_search(q=key, count=10):
# 		username = item.username
# 		dp = item.profile_picture
# 		did = item.id
# 		web = item.website

# 		bio = item.bio
# 		print dp, username, did,web, bio
# 	lol = "text"
# 	return lol
# @app.route('/instagram/media/<path:key>')
# def instagram(key):
# 	api = InstagramAPI(client_id='b64f54dc4fb3486f87b55d92381e2625', client_secret='b5fa80c366b94cc980c882855630fe92')
# 	for item in api.user_recent_media(user_id=key, count=20, max_id=100):
# 		photo = item.images
# 		print dp, username, did,web, bio
# 	lol = "text"
# 	return lol

# @app.route('/instagram')
# def instagram():
# 	api = InstagramAPI(client_id='14c7fb94b134473d9ee9cc449face034', client_secret='1738e7489ef24de0abef9a0dbfa8d3ea')
# 	wew = api.create_subscription(object='tag', object_id='fox', aspect='media', callback_url='http://localhost')
# 	for media in wew:
# 		lol = media.images['standard_resolution'].url
# 		print media.images['standard_resolution'].url
# 	return lol


@app.route('/admin/enable/<path:topic>',methods=['GET','POST'])
def able(topic):
	form = forms.Admin(request.form)
	trends = models.Trace.query.filter_by(tweet=topic).order_by(models.Trace.id.desc())
	if request.method == 'POST':
		value = request.form.getlist('check')
		en_val = request.form.has_key('submit-enable')
		
		db.session.query(models.Trace).\
					filter(models.Trace.id.in_([int(num_string) for num_string in value])).\
					update({models.Trace.enable : en_val}, synchronize_session=False)

		db.session.commit()
		return render_template('admin.html', result=trends, form=form)
	else:
		return render_template('admin.html', result=trends, form=form)









sched.start()
print "end of line"
logging.basicConfig()


admin = Admin(app)
