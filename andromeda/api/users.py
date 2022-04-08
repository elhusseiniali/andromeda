from andromeda.schemas import UserSchema
from andromeda.daos import user_dao
from andromeda.service.user_services import user_service

from flask_restx import Namespace, Resource, fields
from flask import request


api = Namespace('users', description='User related operations')
user_schema = UserSchema()


@api.route('/')
class Users(Resource):

    @api.doc(description="Get all users from the database.")
    def get(self):
        all_users = user_dao.get_all()
        return user_schema.dump(all_users, many=True)

    @api.doc(params={"username": "user username",
                     "email": "user email",
                     "password": "user password",
                     "phone_number": "user internationl number"},
             description="Add a user to the database.",
             responses={201: "This user was created successfully.",
                        422: "Request failed. The parameters were"
                             " valid but the request failed.",
                        400: "Bad Request. Might have"
                             " a missing required parameter."})
    def post(self):
        #  Shouldn't we take json instead?
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')
        phone_number = request.args.get('phone_number')

        if not(username is None) and \
           not(email is None) and \
           not(password is None):
            try:
                user_service.create_user(username=username,
                                         email=email,
                                         password=password,
                                         phone_number=phone_number)

                return "The user was created successfully.", 201

            except Exception as e:
                print(e)
                api.abort(422, e, status="Could not save information",
                          statusCode="422")

        api.abort(400, "Bad Request. Might have a missing required parameter.",
                  status="Could not save information", statusCode="400")


# TODO: Add an update method, and delete.
@api.route('/id=<int:id>')
class getUser(Resource):

    @api.doc(description="Get a user by id from the database.",
             responses={404: "The user was not found.",
                        200: "The user was found."})
    def get(self, id=None):
        user = user_dao.get_by_id(id=id)

        if not(user is None):
            return user_schema.dump(user)

        api.abort(404, message="The user was not found.",
                  status="Could not find information", statusCode="404")


# NOTE: We need to import bookings marshmallow schema to send a
# serialized object. However, this function was just made to test
# the functionality for the time being. Please, update this when
# bookings api is created.
@api.route('/id=<int:id>/bookings')
@api.doc(description="Get a user's bookings by id from the database.",
         responses={404: "The user was not found.",
                    200: "The user's bookings were found."})
class getUserBookings(Resource):

    def get(self, id=None):
        user = user_dao.get_by_id(id=id)

        if not(user is None):
            bookings = user_dao.get_bookings(id=id)
            return bookings

        api.abort(404, message="The user was not found.",
                  status="Could not find information", statusCode="404")
