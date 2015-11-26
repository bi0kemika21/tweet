from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, RadioField, SelectMultipleField, widgets
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class SearchForm(Form):
	searchKeyword = TextField('Search Keyword', [ validators.Required(), validators.Length(min=2, max=140)])

class SearchTrace(Form):
    searchTrace = TextField('Search Keyword', [ validators.Required(), validators.Length(min=2, max=140)])


class Trace(Form):
    filterText = TextAreaField('For Filtering Text and Twitter Name', [ validators.Optional(), validators.Length(min=2, max=200)])

class Admin(Form):
    enable = SelectMultipleField('', choices=[(True,'')],option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
 