import twitter, json
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/trends/<path:country_code>')
def get_trending_keywords(country_code):

	country_code = country_code.upper()
	CONSUMER_KEY = 'd7tKl4qajMQmpwjIbPw'
	CONSUMER_SECRET ='v5Utf5ewYrKdLe7VIHiNLBiPehSdG5gDoqEbPfHRB8A'
	OAUTH_TOKEN = '126343897-sT0c0Fpt6qzrd91TiBbGlPWS3Uov9Z1yhtG6c2on'
	OAUTH_TOKEN_SECRET = 'uFe1tYjoxX5Tf0o5NjHo0wKxTyzvGEPL3GmoRp0LlCDkD'

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

	twitter_api = twitter.Twitter(auth=auth)
	
	WOE_ID = {'global':1, 
				'PH':23424934,
				'US':23424977
	}

	
	if country_code in WOE_ID:
		# print  "Country exists"+country_code
		country_exists = True
	else:
		country_exists = False
		# return "Sorry this feature is not available"+country_code



	if country_exists:
		trends_results = twitter_api.trends.place(_id=WOE_ID[country_code])
				
		julian = []

		for child in trends_results:

			if child['trends']:
	    			for subchild in child['trends']:
	        			
	        			if subchild['name']:
	        				julian.append(subchild['name'])
	        				print subchild['name']

		return 'Got trending keywords from Twitter  in  %s' % country_code;		
		
	else:
		message =  'This feature is not available for this country'
		result =  message
		
	
	






@app.route('/search/<path:keyword>')
def search_keyword(keyword):
	q = '#pba' 
	count = 30	
	lang = 'us' #tl
	result_type = 'popular'
	until ='2014-03-21'

	search_results = twitter_api.search.tweets(q=q, count=count,  until=until)
	statuses = search_results['statuses']
	# print statuses

	for _ in range(5):
		print "Length of statuses", len(statuses)
		# try:
			# next_results = search_results['search_metadata']['next_results']
		# except KeyError, e: # No more results when next_results doesn't exist
			# break

	return 'Search for' + keyword


@app.route('/')
def hello_world():
	return 'Welcome to index page!'



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
		app.run(debug=True)