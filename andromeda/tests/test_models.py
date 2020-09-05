import unittest
from andromeda import Country, City
from andromeda import Company
from andromeda import User, Passport, Employment
from andromeda import Flight, Booking

from datetime import datetime


class TestObjectCreation(unittest.TestCase):
    def test_booking(self):
        france = Country(name="France")
        germany = Country(name="Germany")

        assert france
        assert germany

        paris = City(name="Paris", country=france)
        berlin = City(name="Berlin", country=germany)

        assert paris
        assert berlin

        mrh26 = User(username="mrh26",
                     email="justatest@gmail.com",
                     password="1234",
                     phone_number="+96170405060")

        assert mrh26

        andromeda = Company(name="Andromeda",
                            email="company@gmail.com",
                            phone_number="+96170404040",
                            ticket_quota=10)

        assert andromeda

        employment1 = Employment(user=mrh26, company=andromeda)

        assert employment1

        passport1 = Passport(user=mrh26,
                             first_name="Bratan",
                             last_name="The Tester",
                             date_of_birth="1998-02-12",
                             country=france,
                             issue_date="2020-08-20",
                             expiration_date="2021-08-20")

        assert passport1

        flight1 = Flight(name="MEA200",
                         departure_city=berlin,
                         arrival_city=paris,
                         departure="2020-09-04 23:30:00",
                         arrival="2020-09-05 04:30:00")

        assert flight1

        booking = Booking(flight=flight1,
                          user=mrh26,
                          issuing_employment=employment1,
                          date_issued=datetime.now(),
                          cancellation_deadline="2020-09-01",
                          cancellation_fee=0)

        assert booking
