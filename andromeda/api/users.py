from flask_restx import Namespace, Resource, fields

api = Namespace('users', description='User related operations')


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
