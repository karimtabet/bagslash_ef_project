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

admin.add_view(ModelView(Redirect, db.session))

@app.route('/')
def index():
    return 'Hello'

if __name__ == '__main__':
    app.run()
