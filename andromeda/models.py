from andromeda import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_validator import ValidateEmail, ValidateCountry
from andromeda.custom_validators import ValidatePhoneNumber
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))

    _password = db.Column(db.String(128), nullable=False)

    passport = db.relationship('Passport',
                               back_populates="user",
                               uselist=False,
                               lazy=False)
    employment = db.relationship('Employment',
                                 back_populates="user",
                                 uselist=False,
                                 lazy=True)
    bookings = db.relationship('Booking',
                               back_populates="user",
                               lazy=True)

    def __init__(self,
                 username, email,
                 password,
                 phone_number=None):
        self.username = username
        self.email = email

        self.password = password
        self.phone_number = phone_number

    def __repr__(self):
        return (f"User('{self.id}: {self.username}','{self.email}')")

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
                      message="The e-mail is invalid.")
        ValidatePhoneNumber(User.phone_number,
                            allow_null=True,
                            throw_exception=True,
                            message="Phone number is invalid.")


class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))
    ticket_quota = db.Column(db.Integer, default=0)

    employees = db.relationship('Employment',
                                back_populates="company",
                                lazy=True)

    def __init__(self, name, email, phone_number, ticket_quota):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.ticket_quota = ticket_quota

    def __repr__(self):
        return (f"Company('{self.id}: "
                f"{self.name}', '{self.email}')")

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(Company.email,
                      allow_smtputf8=True,
                      check_deliverability=True,
                      throw_exception=True,
                      message="The e-mail is invalid.")
        ValidatePhoneNumber(Company.phone_number,
                            allow_null=True,
                            throw_exception=True,
                            message="Phone number is invalid.")


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(60), unique=True, nullable=False)

    cities = db.relationship('City',
                             back_populates="country",
                             lazy=True)
    passports = db.relationship('Passport',
                                back_populates="country",
                                lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Country('{self.id}: {self.name}')")

    @classmethod
    def __declare_last__(cls):
        ValidateCountry(Country.name,
                        allow_null=False,
                        throw_exception=True,
                        message="This country does not exist.")


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), nullable=False)

    country_id = db.Column(db.Integer,
                           db.ForeignKey('country.id'),
                           nullable=False)
    country = db.relationship('Country',
                              back_populates="cities",
                              lazy=True)
    arrivals = db.relationship('Flight',
                               foreign_keys="Flight.arrival_city_id",
                               back_populates="arrival_city",
                               lazy=True)
    departures = db.relationship('Flight',
                                 foreign_keys="Flight.departure_city_id",
                                 back_populates="departure_city",
                                 lazy=True)

    def __init__(self, name, country):
        self.name = name
        self.country = country

    def __repr__(self):
        return (f"City('{self.id}': '{self.name}')")


class Passport(db.Model):
    __tablename__ = "passport"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        primary_key=True)
    user = db.relationship('User',
                           back_populates="passport",
                           lazy=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)

    country_id = db.Column(db.Integer,
                           db.ForeignKey('country.id'),
                           nullable=False)
    country = db.relationship('Country',
                              back_populates="passports",
                              lazy=True)

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

    arrival = db.Column(db.DateTime, nullable=False)
    arrival_city_id = db.Column(db.Integer,
                                db.ForeignKey('city.id'),
                                nullable=False)
    arrival_city = db.relationship('City',
                                   foreign_keys=arrival_city_id,
                                   back_populates="arrivals",
                                   lazy=True)

    departure = db.Column(db.DateTime, nullable=False)
    departure_city_id = db.Column(db.Integer,
                                  db.ForeignKey('city.id'),
                                  nullable=False)
    departure_city = db.relationship('City',
                                     foreign_keys=departure_city_id,
                                     back_populates="departures",
                                     lazy=True)

    bookings = db.relationship('Booking',
                               back_populates="flight",
                               lazy=True)

    def __init__(self, flight_id, name,
                 departure_city_id, arrival_city_id,
                 departure, arrival):
        self.flight_id = flight_id
        self.name = name
        self.departure_city_id = departure_city_id
        self.arrival_city_id = arrival_city_id
        self.departure = departure
        self.arrival = arrival

    def __repr__(self):
        return (f"Flight('{self.name}', '{self.departure_city_id}',"
                f"'{self.arrival_city_id}')")


class Employment(db.Model):
    __tablename__ = "employment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User',
                           back_populates="employment",
                           lazy=True)

    company_id = db.Column(db.Integer,
                           db.ForeignKey('company.id'),
                           nullable=False)
    company = db.relationship('Company',
                              back_populates="employees",
                              lazy=True)

    bookings = db.relationship('Booking',
                               back_populates="employment",
                               lazy=True)

    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id

    def __repr__(self):
        return f"Employment('{self.user}', '{self.company}')"


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_id = db.Column(db.Integer,
                          db.ForeignKey('flight.id'),
                          nullable=False)
    flight = db.relationship('Flight',
                             back_populates="bookings",
                             lazy=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship('User',
                           back_populates="bookings",
                           lazy=True)

    date_issued = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            nullable=False)

    issuing_employment_id = db.Column(db.Integer,
                                      db.ForeignKey('employment.user_id'),
                                      nullable=False)
    employment = db.relationship('Employment',
                                 back_populates="bookings",
                                 lazy=True)

    cancellation_fee = db.Column(db.Float, default=0)
    cancellation_deadline = db.Column(db.Date, nullable=False)

    def __init__(self, flight_id,
                 user_id, issuing_employment_id, date_issued,
                 cancellation_fee, cancellation_deadline):
        self.flight_id = flight_id
        self.user_id = user_id
        self.issuing_employment_id = issuing_employment_id
        self.date_issued = date_issued
        self.cancellation_fee = cancellation_fee
        self.cancellation_deadline = cancellation_deadline

    def __repr__(self):
        return (f"Booking('ID: {self.id}', "
                f"'User: {self.user_id}', "
                f"'Flight: {self.flight_id}')")
