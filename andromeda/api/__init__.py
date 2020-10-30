from flask import Blueprint
from flask_restx import Api

from andromeda.api.users import api as ns1

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='ANDROMEDA API',
          version='1.0',
          description='Manage a flights booking system.')

api.add_namespace(ns1)
