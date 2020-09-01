from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SECURITY_PASSWORD_SCHEMES'] = ['pbkdf2_sha512']

#    CACHING FIX FOR PRODUCTION ONLY
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#   Below import is necessary, even if the linter complains about it.
#   This is because the linter cannot distinguish between imports in a script
#   and imports in a package. The order of the imports is also important.
#   These two imports *had* to happen after initializing db.
from andromeda import routes
from andromeda.models import User, Company, Country, City, Passport
from andromeda.models import Flight, Employment, Booking

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

# Show null values instead of empty strings.
MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({type(None): typefmt.null_formatter})


class UserView(ModelView):
    form_columns = (
        'username',
        'email',
        'password',
        'phone_number',
    )
    column_editable_list = ('username', 'email', 'phone_number')
    column_searchable_list = ('username', 'email')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class CountryView(ModelView):
    form_excluded_columns = ('cities', 'passport', 'passports')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class CityView(ModelView):
    form_columns = ('name', 'country')
    column_list = ('name', 'country')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class PassportView(ModelView):
    column_labels = dict(user_country='Country')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class FlightView(ModelView):
    column_list = ('name',
                   'origin_city',
                   'destination_city',
                   'departure',
                   'arrival')
    form_columns = ('name',
                    'origin_city',
                    'destination_city',
                    'departure',
                    'arrival')
    column_labels = dict(origin_city='From',
                         destination_city='To',
                         departure='Departure Time',
                         arrival='Arrival Time')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class CompanyView(ModelView):
    form_excluded_columns = ('employees')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class EmploymentView(ModelView):
    form_excluded_columns = ('bookings')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class BookingView(ModelView):
    column_list = ('user',
                   'flight',
                   'employment',
                   'date_issued',
                   'cancellation_fee',
                   'cancellation_deadline')
    form_columns = ('user',
                    'flight',
                    'employment',
                    'date_issued',
                    'cancellation_fee',
                    'cancellation_deadline')
    column_type_formatters = MY_DEFAULT_FORMATTERS


admin = Admin(app, name='Andromeda Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(UserView(User, db.session))
admin.add_view(CompanyView(Company, db.session))
admin.add_view(CountryView(Country, db.session))
admin.add_view(CityView(City, db.session))
admin.add_view(PassportView(Passport, db.session))
admin.add_view(FlightView(Flight, db.session))
admin.add_view(EmploymentView(Employment, db.session))
admin.add_view(BookingView(Booking, db.session))
