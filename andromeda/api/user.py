from flask_restx import Namespace, Resource, fields

from andromeda.models import User, db

api = Namespace('user', description='User related operations')

user = api.model('user', {
    'username': fields.String(required=True, description='user username'),
    'email': fields.String(required=True, description='user email address'),
    'password': fields.String(required=True, description='user password'),
    'phone_number': fields.String(required=False,
                                  description='user international'
                                              ' phone number')
})


# TODO: Add service foldder to add user CRUD class.
# TODO: Figure out how to give get and post different descriptions.
# TODO: Incorporate Flask_marhmallow.

@api.route('/')
class GetAllUsers(Resource):
    @api.marshal_list_with(user)
    def get(self):
        return User.query.all()

    # TODO: Take arguments from parameters and not payload.
    # TODO: Remove this function from here. Consider adding this in
    # it's own class instead of a part of another.
    @api.expect(user, validate=True)
    @api.marshal_with(user, code=201)
    @api.response(409, "This user already exists")
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


@api.route('/id=<int:id>',
           doc={'description': 'Get User from user id.'})
class getUser(Resource):
    @api.response(404, "This user doesn't exist")
    @api.marshal_with(user)
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return api.abort(404, "This user doesn't exists")

        else:
            return user, 200
