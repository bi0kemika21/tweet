from instagram.client import InstagramAPI
import app
from flask import Flask, redirect, url_for, session, request
from flask import Response, stream_with_context
import httplib2
from flask import Flask, render_template, request, jsonify
import json
import sys
import types
try:
    import simplejson as json
except ImportError:
    import json
import getpass
import unittest
import urlparse
app = Flask(__name__)

access_token = "1293852108.b64f54d.033d7fb80e444c04aef03a7e601b93f6"

@app.route('/authorize-instagram')
def authorize_instagram():
    from instagram import client

    redirect_uri = (util.get_host() + url_for('handle_instagram_authorization'))
    instagram_client = client.InstagramAPI(client_id=INSTAGRAM_CLIENT, client_secret=INSTAGRAM_SECRET, redirect_uri=redirect_uri)
    return redirect(instagram_client.get_authorize_url(scope=['basic']))
@app.route('/handle-instagram-authorization')
def handle_instagram_authorization():
    from instagram import client

    code = request.values.get('code')
    if not code:
        return error_response('Missing code')
    try:
        redirect_uri = (util.get_host() + url_for('handle_instagram_authorization'))
        instagram_client = client.InstagramAPI(client_id=INSTAGRAM_CLIENT, client_secret=INSTAGRAM_SECRET, redirect_uri=redirect_uri)
        access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
        if not access_token:
            return error_response('Could not get access token')
        g.user.instagram_userid = instagram_user['id']
        g.user.instagram_auth   = access_token
        g.user.save()
        deferred.defer(fetch_instagram_for_user, g.user.get_id(), count=20, _queue='instagram')
    except Exception, e:
        return error_response('Error')
    return redirect(url_for('settings_data') + '?after_instagram_auth=True')
def fetch_instagram_for_user(user_id, count=3):
    from instagram import client

    user = models.User.get_by_id(user_id)
    if not user.instagram_auth or not user.instagram_userid:
        return

    instagram_client = client.InstagramAPI(access_token=access_token)
    recent_media, next = instagram_client.user_recent_media(user_id=user.instagram_userid, count=count)
    for media in recent_media:
        tags = []
        for tag in media.tags:
            tags.append(tag.name.lower())
        if not ('eatdifferent' in tags or 'ed' in tags):
            continue
        cache_key = 'instagram-%s-%s' % (user.get_id(), media.id)
        if util.get_from_cache(cache_key) and False:
            continue
        imports.import_instagram(user, media)
        util.put_in_cache(cache_key, 'true')
        instagram_client = client.InstagramAPI(client_id=INSTAGRAM_CLIENT, client_secret=INSTAGRAM_SECRET)
        callback_url = 'http://www.eatdifferent.com/hook/parse-instagram'
        instagram_client.create_subscription(object='user', aspect='media', callback_url=callback_url)
@app.route('/hook/parse-instagram')
def parse_instagram():
    from instagram import client, subscriptions

    mode         = request.values.get('hub.mode')
    challenge    = request.values.get('hub.challenge')
    verify_token = request.values.get('hub.verify_token')
    if challenge: 
        return Response(challenge)
    else:
        reactor = subscriptions.SubscriptionsReactor()
        reactor.register_callback(subscriptions.SubscriptionType.USER, parse_instagram_update)

        x_hub_signature = request.headers.get('X-Hub-Signature')
        raw_response    = request.data
        try:
            reactor.process(INSTAGRAM_SECRET, raw_response, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            logging.error('Instagram signature mismatch')
    return Response('Parsed instagram')
def parse_instagram_update(update):
    instagram_userid = update['object_id']
    users = models.User.all().filter('instagram_userid =', instagram_userid).fetch(10)
    if len(users) == 0:
        logging.info('Didnt find matching users for this update')
    for user in users:
        deferred.defer(fetch_instagram_for_user, user.get_id(), _queue='instagram', _countdown=120)


app.run(debug = True, port = 2000)
