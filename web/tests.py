from datetime import datetime

from flask.ext.testing import TestCase
from hamcrest import assert_that, is_, has_length

from app import app, db, get_redirect, get_random_string
from models import Base, Redirect


class TestRedirects(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.app = app.test_client()

        for table in reversed(Base.metadata.sorted_tables):
            db.session.execute(table.delete())

    def insert_redirect(self):
        redirect = Redirect(
            from_url='test_url',
            to_url='https://www.example.com',
            times_accessed=0,
            date_created=datetime.utcnow()
        )
        db.session.add(redirect)
        return redirect

    def test_get_redirect(self):
        self.insert_redirect()
        assert_that(
            get_redirect('test_url'),
            is_('https://www.example.com')
        )

    def test_get_random_string(self):
        assert_that(
            get_random_string(),
            has_length(23)
        )

    def test_successful_redirect(self):
        self.insert_redirect()
        response = self.app.get('/test_url')
        assert_that(
            response.status_code,
            is_(302)
        )
