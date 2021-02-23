"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

from sqlalchemy import exc


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ["DATABASE_URL"] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser", email="test@test.com", password="testuser", image_url=None)

        db.session.commit()

    def test_message_model(self):
        """Does basic message model work?"""

        # Create test user
        msg = Message(text="message text", user_id=self.testuser.id)
        db.session.add(msg)
        db.session.commit()

        # Retrieve all messages from table
        msg = Message.query.all()
        # should be only one message
        self.assertEqual(len(msg), 1)
        # Retrieve only message
        msg = Message.query.one()
        # Check text corret
        self.assertEqual(msg.text, "message text")
        # Check user_id correct
        self.assertEqual(msg.user_id, self.testuser.id)
