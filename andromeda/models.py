from andromeda import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_validator import ValidateEmail, ValidateCountry


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)  # Hashed Password
    phone_number = db.Column(db.String(30))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    @classmethod
    def __declare_last__(cls):
        # Check available validators:
        # https://flask-validator.readthedocs.io/en/latest/
        # TODO: handle exception properly in admin panel
        ValidateEmail(User.email,
                      allow_smtputf8=True,
                      check_deliverability=True,
                      throw_exception=True,
                      message="The e-mail is invalid. Please check it.")

    def __init__(self, username, email, password, phone_number=None):
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def __repr__(self):
        return (f"User('{self.username}','{self.email}')")


class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))
    ticket_quota = db.Column(db.Integer)

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Company.email,
                      allow_smtputf8=True,
                      check_deliverability=True,
                      throw_exception=True,
                      message="The e-mail is invalid. Please check it.")

    def __init__(self, name, email, phone_number=None, ticket_quota=0):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.ticket_quota = ticket_quota

    def __repr__(self):
        return f"Company('{self.name}', '{self.email}')"


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    cities = db.relationship('City',
                             back_populates="country",
                             lazy=True)

    @classmethod
    def __declare_last__(cls):
        ValidateCountry(Country.name,
                        allow_null=False,
                        throw_exception=True,
                        message="This country does not exist.")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Country('{self.name}')")


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)  # Not unique
    country_id = db.Column(db.Integer,
                           db.ForeignKey('country.id'),
                           nullable=False)
    country = db.relationship('Country',
                              back_populates="cities",
                              lazy=True)

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def __repr__(self):
        return (f"City('{self.name}', '{self.country_id}')")
