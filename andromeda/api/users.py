from flask_restx import Namespace, Resource, fields

from andromeda.models import User, db

api = Namespace('users', description='User related operations')

user = api.model('user', {
    'username': fields.String(required=True, description='user username'),
    'email': fields.String(required=True, description='user email address'),
    'password': fields.String(required=True, description='user password'),
    'phone_number': fields.String(required=False,
                                  description='user international'
                                              ' phone number')
})


@api.route('/')
class UserList(Resource):

    @api.doc('get all users')
    @api.marshal_list_with(user)
    def get(self):
        return User.query.all()

    @api.doc('create_user')
    @api.expect(user)
    @api.marshal_with(user, code=201)
    def post(self):
        data = api.payload

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            new_user = User(username=data['username'],
                            email=data['email'],
                            password=data['password'],
                            phone_number=data['phone_number'])

            db.session.add(new_user)
            db.session.commit()

            return new_user, 201
        else:
            # Error code 409: resource (user) already exists.
            return api.abort(409, "This user already exists")
