from datetime import datetime
from uuid import uuid4

from flask import (
    Flask,
    redirect,
    session,
    g,
    url_for,
    request,
    flash
)
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin.model.template import macro
from rauth.service import OAuth1Service
from rauth.utils import parse_utf8_qsl

from models import Redirect, User
from utils import get_random_string, add_http_to_url
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')

twitter = OAuth1Service(
    name='twitter',
    consumer_key=app.config['TWITTER_CONSUMER_KEY'],
    consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/'
)


@app.before_request
def before_request():
    g.user = None
    if 'user_uuid' in session:
        g.user = db.session.query(User).filter(
            User.uuid == session['user_uuid']
        )


@app.after_request
def after_request(response):
    db.session.remove()
    return response


@app.route('/')
def index():
    if g.user:
        return redirect('/admin/redirects_view')
    else:
        return redirect('/admin')


@app.route('/twitter/login')
def login():
    oauth_callback = url_for('authorized', _external=True)
    params = {'oauth_callback': oauth_callback}
    r = twitter.get_raw_request_token(params=params)
    data = parse_utf8_qsl(r.content)

    session['twitter_oauth'] = (data['oauth_token'],
                                data['oauth_token_secret'])
    return redirect(twitter.get_authorize_url(data['oauth_token'], **params))


@app.route('/twitter/authorized')
def authorized():
    request_token, request_token_secret = session.pop('twitter_oauth')

    # check to make sure the user authorized the request
    if 'oauth_token' not in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    try:
        creds = {
            'request_token': request_token,
            'request_token_secret': request_token_secret
            }
        params = {'oauth_verifier': request.args['oauth_verifier']}
        sess = twitter.get_auth_session(params=params, **creds)
    except Exception as e:
        flash('There was a problem logging into Twitter: ' + str(e))
        return redirect(url_for('index'))

    verify = sess.get(
        'account/verify_credentials.json',
        params={'format': 'json'}
    ).json()

    user = db.session.query(User).filter(
        User.name == verify['screen_name']
    ).first()
    if user is None:
        user = User(verify['screen_name'])
        db.session.add(user)
        db.session.commit()

    session['user_uuid'] = user.uuid

    flash('Logged in as ' + verify['name'])
    return redirect(url_for('index'))


def get_redirect(custom_url):
    redirect = db.session.query(Redirect).filter(
        Redirect.from_url == custom_url
    ).first()
    redirect.times_accessed += 1
    db.session.add(redirect)
    db.session.commit()
    return redirect


@app.route('/to/<custom_url>', methods=['GET'])
def redirct(custom_url):
    return redirect(get_redirect(custom_url).to_url)


class RedirectsView(ModelView):
    def is_accessible(self):
        return g.user is not None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index', next=request.url))

    can_edit = False
    list_template = "list_redirects.html"
    column_list = column_sortable_list = column_filters = (
        'from_url',
        'to_url',
        'times_accessed',
        'user.name',
        'date_created'
    )
    column_searchable_list = ('from_url', 'to_url')
    column_labels = {"user.name": "Created By"}
    column_formatters = {
        'from_url': macro("from_url"),
        'to_url': macro('to_url')
    }
    form_columns = ['from_url', 'to_url']
    form_args = dict(
                from_url=dict(default=get_random_string())
            )

    def on_model_change(self, form, model):
        model.redirect_uuid = uuid4
        model.from_url = form.from_url.data
        model.to_url = add_http_to_url(form.to_url.data)
        model.times_accessed = 0
        model.created_by = session['user_uuid']
        model.date_created = datetime.utcnow()

admin.add_view(RedirectsView(
    Redirect,
    db.session,
    name='Redirects',
    endpoint='redirects_view')
)

if __name__ == '__main__':
    app.run()
