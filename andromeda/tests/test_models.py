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

        mrh26 = User("mrh26", "mariahajj5@gmail.com", "1234", "+96170401523")

        assert mrh26

        andromeda = Company("Andromeda",
                            "mariahajj5@gmail.com",
                            "+96170401523",
                            10)

        assert andromeda

        employment1 = Employment(mrh26, andromeda)

        assert employment1

        passport1 = Passport("Maria", "Hajj",
                             "1998-02-12", france,
                             "2020-08-20", "2021-08-20")

        assert passport1

        flight1 = Flight("MEA200", berlin, paris,
                         "2020-09-04 23:30:00", "2020-09-05 04:30:00")

        assert flight1

        booking = Booking(flight1, mrh26, employment1,
                          "2020-09-01", date_issued=datetime.now(),
                          cancellation_fee=0)

        assert booking

