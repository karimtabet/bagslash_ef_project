from datetime import datetime
from uuid import uuid4

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import Redirect
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')


class RedirectsView(ModelView):
    can_edit = False
    column_list = column_sortable_list = column_filters = (
        'from_url',
        'to_url',
        'times_accessed',
        'date_created'
    )
    column_searchable_list = ('from_url', 'to_url')
    form_columns = ['from_url', 'to_url']

    def on_model_change(self, form, model):
        model.redirect_uuid = uuid4
        model.from_url = form.from_url.data
        model.to_url = form.to_url.data
        model.times_accessed = 0
        model.date_created = datetime.utcnow()

admin.add_view(RedirectsView(Redirect, db.session, endpoint='redirects_view'))


@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run()
