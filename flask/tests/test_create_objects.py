# -------------------------------------------------------------------------------
# Every test file should come in pairs: a base file and the file containing
# the tests. An exception to that is the 'test_configs.py' because it is
# very simple.
#
# This is the file that contains the tests.
#
# You can call this test group file to run by running the application and
# running 'docker-compose run --rm flask python manage.py test_one test_website'
# in a separate terminal window.
# -------------------------------------------------------------------------------


import unittest
import json
from tests.base_create_objects import BaseTestCase
from project.services.electronics import create_desktop, create_laptop, create_tablet, create_monitor, create_television, \
    validate_price, validate_weight, validate_ram_size, validate_cpu_cores, validate_hd_size
from tests.helpers import make_auth_header
from flask import g


# This class inherits from the base class in 'base_website.py', in order to
# get the create_app, setUp and tearDown methods.
class TestAuthentication(BaseTestCase):
    def test_if_price_is_valid(self):
        with self.client:
            self.assertTrue(validate_price(99))
            self.assertFalse(validate_price(-1))

    def test_if_weight_is_valid(self):
        with self.client:
            self.assertTrue(validate_weight(99))
            self.assertFalse(validate_weight(-1))

    def test_if_ram_size_is_valid(self):
        with self.client:
            self.assertTrue(validate_ram_size(8))
            self.assertFalse(validate_ram_size(6))
            self.assertFalse(validate_ram_size(-1))

    def test_if_cpu_cores_is_valid(self):
        with self.client:
            self.assertTrue(validate_cpu_cores(4))
            self.assertTrue(validate_cpu_cores(2))
            self.assertFalse(validate_cpu_cores(7))
            self.assertFalse(validate_cpu_cores(-4))

    def test_if_hd_size_is_valid(self):
        with self.client:
            self.assertTrue(validate_hd_size(99))
            self.assertFalse(validate_hd_size(-1))

    def test_create_desktop_object(self):
        with self.client:
            desktop = create_desktop(500, 100, "LG", "intel", 32, 4, 20, "20x20")

            self.assertEqual(desktop.price, 500)
            self.assertEqual(desktop.weight, 100)
            self.assertEqual(desktop.brand, "LG")
            self.assertEqual(desktop.processor, "intel")
            self.assertEqual(desktop.ram_size, 32)
            self.assertEqual(desktop.cpu_cores, 4)
            self.assertEqual(desktop.hd_size, 20)
            self.assertEqual(desktop.dimensions, "20x20")

    def test_create_laptop_object(self):
        with self.client:
            laptop = create_laptop(600, 200, "LG", "32x32", "intel", 64, 2, 40, "Long lasting battery", "Windows 10", False, True)

            self.assertEqual(laptop.price, 600)
            self.assertEqual(laptop.weight, 200)
            self.assertEqual(laptop.brand, "LG")
            self.assertEqual(laptop.display_size, "32x32")
            self.assertEqual(laptop.processor, "intel")
            self.assertEqual(laptop.ram_size, 64)
            self.assertEqual(laptop.cpu_cores, 2)
            self.assertEqual(laptop.hd_size, 40)
            self.assertEqual(laptop.battery_info, "Long lasting battery")
            self.assertEqual(laptop.os, "Windows 10")
            self.assertEqual(laptop.touchscreen, False)
            self.assertEqual(laptop.camera, True)

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
