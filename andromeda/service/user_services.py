# https://levelup.gitconnected.com/structuring-a-large-production-flask-application-7a0066a65447

from andromeda.daos import user_dao, User, db


class UserService():
    __instance__ = None

    def __init__(self):
        if UserService.__instance__ is None:
            UserService.__instance__ = self
        else:
            raise Exception("You cannot create another UserService class")

    @staticmethod
    def get_instance():
        if not UserService.__instance__:
            UserService()
        return UserService.__instance__

    def create_user(self, username, email, password, phone_number=None):

        if (username is None) and (email is None) and (email is None) \
           and (password is None):
            return None

        user = user_dao.get_by_username(username=username)

        if user is None:
            user = User(username=username,
                        email=email.casefold(),
                        password=password,
                        phone_number=phone_number)

            user_dao.add(user)

            return user

        # Should we raise an exception?
        return None

    def update_user(self, id, username=None, email=None, phone_number=None):
        if(id is None):
            return False

        if (phone_number is None) and (username is None) and (email is None):
            return False

        try:
            user = user_dao.get_by_id(id=id)

            if username:
                user.username = username
            if email:
                user.email = email
            if phone_number:
                user.phone_number = phone_number

            db.session.commit()

            return True

        except Exception:
            return False

    def delete_user(self, id):
        if id is None:
            return False

        try:
            user = user_dao.get_by_id(id=id)

            user.delete()
            db.session.commit()

            return True

        except Exception:
            return False


user_service = UserService()
