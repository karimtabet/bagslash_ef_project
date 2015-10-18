from datetime import datetime

from flask.ext.testing import TestCase
from hamcrest import assert_that, is_

from app import app, db
from models import Base, Redirect


class TestRedirects(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.app = app.test_client()

        for table in reversed(Base.metadata.sorted_tables):
            db.session.execute(table.delete())

    def test_successful_redirect(self):
        redirect = Redirect(
            from_url='test_url',
            to_url='www.example.com',
            times_accessed=0,
            date_created=datetime.utcnow()
        )
        db.session.add(redirect)

        response = self.app.get('/test_url')
        assert_that(
            response.status_code,
            is_(302)
        )
