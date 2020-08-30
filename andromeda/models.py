from andromeda import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_validator import ValidateEmail, ValidateCountry
from andromeda.custom_validators import ValidatePhoneNumber


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
    passports = db.relationship('Passport',
                                back_populates="user",
                                lazy=True)

    def __init__(self, username, email, password, phone_number=None):
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def __repr__(self):
        return (f"User('{self.username}','{self.email}')")

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
        ValidatePhoneNumber(User.phone_number,
                            allow_null=True,
                            throw_exception=True,
                            message="Phone Number is invalid.")


class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))
    ticket_quota = db.Column(db.Integer, default=0)

    def __init__(self, name, email, phone_number=None, ticket_quota=0):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.ticket_quota = ticket_quota

    def __repr__(self):
        return f"Company('{self.name}', '{self.email}')"

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Company.email,
                      allow_smtputf8=True,
                      check_deliverability=True,
                      throw_exception=True,
                      message="The e-mail is invalid. Please check it.")


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    cities = db.relationship('City',
                             back_populates="country",
                             lazy=True)
    passports = db.relationship('Passport',
                                back_populates="user_country",
                                lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Country('{self.name}')")

    @classmethod
    def __declare_last__(cls):
        ValidateCountry(Country.name,
                        allow_null=False,
                        throw_exception=True,
                        message="This country does not exist.")


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
    arrivals = db.relationship('Flight',
                               foreign_keys="Flight.destination_city_id",
                               back_populates="destination_city",
                               lazy=True)
    departures = db.relationship('Flight',
                                 foreign_keys="Flight.origin_city_id",
                                 back_populates="origin_city",
                                 lazy=True)

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def __repr__(self):
        return (f"City('{self.name}', '{self.country_id}')")


class Passport(db.Model):
    __tablename__ = "passport"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        primary_key=True)
    user = db.relationship('User',
                           back_populates="passports",
                           lazy=True)
    country_id = db.Column(db.Integer,
                           db.ForeignKey('country.id'),
                           nullable=False)
    user_country = db.relationship('Country',
                                   back_populates="passports",
                                   lazy=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

    def __init__(self, country_id, first_name, last_name, date_of_birth,
                 issue_date, expiration_date):
        self.country_id = country_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.issue_date = issue_date
        self.expiration_date = expiration_date

    def __repr__(self):
        return (f"Passport('{self.first_name}', '{self.last_name}',"
                f"'{self.expiration_date}')")


class Flight(db.Model):
    __tablename__ = "flight"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    departure = db.Column(db.DateTime, nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    destination_city_id = db.Column(db.Integer,
                                    db.ForeignKey('city.id'),
                                    nullable=False)
    destination_city = db.relationship('City',
                                       foreign_keys=destination_city_id,
                                       back_populates="arrivals",
                                       lazy=True)
    origin_city_id = db.Column(db.Integer,
                               db.ForeignKey('city.id'),
                               nullable=False)
    origin_city = db.relationship('City',
                                  foreign_keys=origin_city_id,
                                  back_populates="departures",
                                  lazy=True)

    def __init__(self, name, destination_city_id, origin_city_id, departure,
                 arrival):
        self.name = name
        self.destination_city_id = destination_city_id
        self.origin_city_id = origin_city_id
        self.departure = departure
        self.arrival = arrival

    def __repr__(self):
        return (f"Flight('{self.name}', '{self.destination_city}',"
                f"'{self.origin_city}')")
