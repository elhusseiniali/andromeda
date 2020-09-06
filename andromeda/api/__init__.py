from flask import Blueprint
from flask_restx import Api

from andromeda.api.users import api as ns1

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='ANDROMEDA API',
          version='1.0',
          description='Add Description')

api.add_namespace(ns1)
