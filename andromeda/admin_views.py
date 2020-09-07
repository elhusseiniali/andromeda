from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt


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


class CompanyView(ModelView):
    form_excluded_columns = ('employees')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class CountryView(ModelView):
    form_excluded_columns = ('cities', 'passports')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class CityView(ModelView):
    form_columns = ('name', 'country')
    column_list = ('name', 'country')
    column_type_formatters = MY_DEFAULT_FORMATTERS


class PassportView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS


class FlightView(ModelView):
    column_list = ('name',
                   'departure_city',
                   'arrival_city',
                   'departure',
                   'arrival')
    form_columns = ('name',
                    'departure_city',
                    'arrival_city',
                    'departure',
                    'arrival')
    column_labels = dict(departure_city='From',
                         arrival_city='To',
                         departure='Departure Time',
                         arrival='Arrival Time')
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
