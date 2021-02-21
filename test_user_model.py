"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        # create 1st test user
        u = User(email="test@test.com", username="testuser", password="HASHED_PASSWORD")
        db.session.add(u)
        db.session.commit()

        # User should have no messages, no followers, no following, no likes
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 0)
        self.assertEqual(len(u.likes), 0)

        # check __repr__ operation
        self.assertEqual(repr(u), f"<User #{u.id}: testuser, test@test.com>")

        # create 2nd test user
        u2 = User(email="test2@test2.com", username="testuser2", password="HASHED_PASSWORD")
        db.session.add(u2)
        db.session.commit()

        # Check not follow
        # u2 has to be user object
        self.assertEqual(u.is_following(u2), False)
        self.assertEqual(u.is_followed_by(u2), False)

        # create 2 entries in follows table pointed to each other
        follow = Follows(user_being_followed_id=u.id, user_following_id=u2.id)
        db.session.add(follow)
        db.session.commit()

        follow = Follows(user_being_followed_id=u2.id, user_following_id=u.id)
        db.session.add(follow)
        db.session.commit()

        # check follows
        # parameter u2 has to be a user object
        self.assertEqual(u.is_followed_by(u2), True)
        self.assertEqual(u2.is_followed_by(u), True)

        # create signed in user
        u3 = User.signup("testuser3", "test3@test3.com", "HASHED_PASSWORD", "")
        db.session.commit()
        # check authenticate of signed in user
        good_user = User.authenticate(u3.username, "HASHED_PASSWORD")
        self.assertTrue(good_user)

        # check authenticate of incorrect user name
        good_user = User.authenticate("bad-user-name", "HASHED_PASSWORD")
        self.assertFalse(good_user)

        # check authenticate of incorrect password
        good_user = User.authenticate(u3.username, "bad-password")
        self.assertFalse(good_user)
