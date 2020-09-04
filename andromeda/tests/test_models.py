import unittest
from andromeda import Country, City
from andromeda import Company
from andromeda import User, Passport
from andromeda import Flight, Booking


class TestObjectCreation(unittest.TestCase):
    def test_booking(self):
        france = Country(name="France")
        germany = Country(name="Germany")

        assert france
        assert germany

        paris = City(name="Paris")
        berlin = City(name="Berlin")

        assert paris
        assert berlin
