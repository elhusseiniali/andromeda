from marshmallow import Schema, fields
from marshmallow import pre_load, post_dump, post_load

from andromeda.service.user_services import user_service


class BaseSchema(Schema):
    __envelope__ = {"single": None, "many": None}

    def get_envelope_key(self, many):
        key = self.__envelope__["many"] if many else self \
            .__envelope__["single"]
        assert key is not None, "Envelope key undefined"
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)
        return {key: data}


class UserSchema(BaseSchema):
    __envelope__ = {"single": "user", "many": "users"}

    class Meta:
        ordered = True

    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    phone_number = fields.String(required=False, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return user_service.create_user(**data)
