# https://levelup.gitconnected.com/structuring-a-large-production-flask-application-7a0066a65447

from andromeda.models import User
from andromeda import db


class UserDAO():
    __instance__ = None

    def __init__(self):
        if UserDAO.__instance__ is None:
            UserDAO.__instance__ = self
        else:
            raise Exception("You cannot create another UserDAO class")

    @staticmethod
    def get_instance():
        if not UserDAO.__instance__:
            UserDAO()
        return UserDAO.__instance__

    def add(self, user):
        db.session.add(user)
        db.session.commit()

    def get_all(self):
        return db.session.query(User).all()

    def get_by_id(self, id):
        return db.session.query(User).get(id)

    def get_by_username(self, username):
        return db.session.query(User).filter_by(username=username).first()

    def get_by_email(self, email):
        return db.session.query(User).filter_by(email=email).first()

    def get_bookings(self, id):
        user = self.get_by_id(id=id)
        return user.bookings

    def get_employment(self, id):
        user = self.get_by_id(id=id)
        return user.employment

    def get_passport(self, id):
        user = self.get_by_id(id=id)
        return user.passport


user_dao = UserDAO()
