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

from andromeda.api import blueprint as api
app.register_blueprint(api, url_prefix='/api/v1')

#   Below import is necessary, even if the linter complains about it.
#   This is because the linter cannot distinguish between imports in a script
#   and imports in a package. The order of the imports is also important.
#   These two imports *had* to happen after initializing db.
from andromeda import routes
from andromeda.models import User, Company, Country, City, Passport
from andromeda.models import Flight, Employment, Booking
from andromeda.admin_views import UserView, CompanyView, CountryView, CityView
from andromeda.admin_views import BookingView, EmploymentView, PassportView
from andromeda.admin_views import FlightView

from flask_admin import Admin

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'


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
