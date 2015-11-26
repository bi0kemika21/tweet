from flask import flash, escape, request, Flask, url_for,  redirect, render_template, session
from app import app, models
from forms import LoginForm, RegistrationForm
import twitter, json


# def checkIfLogin():
# 	login = False
# 	if 'username' in session:
# 		# return 'Logged in as %s' % escape(session['username'])
# 		return True
# 	else: 
# 		return redirect(url_for('login'))
# 		return False
# 	# return login


# @app.route('/login', methods = ['GET', 'POST'])
# def loginnew():
# 		form = LoginForm()
# 		if form.validate_on_submit():
# 				flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
# 				return redirect('/index')
# 		return render_template('login_new.html', 
# 				title = 'Sign In',
# 				form = form,
# 				providers = app.config['OPENID_PROVIDERS'])
						

# #@app.route('/login', methods = ['GET', 'POST'])
# #def login():

# #	if checkIfLogin():
# #		return redirect(url_for('show_trends'))
# #	if request.method == 'POST':
# #		session['username'] = request.form['username']
# #		redirect(url_for('home'))
# #		return '22'
	
# # 	return render_template('login.html')
# # 	# return '''
# # 	# <form action="" method="post">
# # 	# <p><input type=text name=username>
# # 	# <p><input type=submit value=Login>
# # 	# </form>
# # 	# ''' 
# # 	if 'username' in session:
# # 		return 'Logged in as %s' % escape(session['username'])
# # 	return 'You are not logged in'

# # 	return 'Login!'
# @app.route('/juliantesting')
# def testurl():
# 	return 'ttetetetsing'

# @app.route('/logout')
# def logout():
# 		# remove the username from the session if it's there
# 		session.pop('username', None)
# 		return redirect(url_for('index'))

# # set the secret key.  keep this really secret:
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# @app.errorhandler(404)
# def page_not_found(error):
# 	# return redirect(url_for('login'))
# 	# return render_template('404.html'), 404
# 	return 404
# # @app.route('/home')
# # def home():
# # 	if( checkIfLogin()):
# # 		return 'this is home'
# # 	else:
# # 		return redirect(url_for('login'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         # user = User(form.username.data, form.email.data,
#         #             form.password.data)
#         # db_session.add(user)
#         flash('Thanks for registeringXX')
#         return redirect(url_for('show_trends'))
#     return render_template('register.html', form=form)