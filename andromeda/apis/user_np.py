from flask_restx import Namespace, Resource, fields

api = Namespace('users', description='User related operations')


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        '''List all users'''
        return "User"
