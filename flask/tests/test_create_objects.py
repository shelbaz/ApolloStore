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
from project.services.electronic_service import ElectronicService
from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.television_service import TelevisionService
from tests.helpers import make_auth_header
from flask import g


# This class inherits from the base class in 'base_create_objects.py', in order to
# get the create_app, setUp and tearDown methods.
class TestCreationObjects(BaseTestCase):
    def test_if_price_is_valid(self):
        with self.client:
            self.assertTrue(ElectronicService.validate_price(99))
            self.assertFalse(ElectronicService.validate_price(-1))

    def test_if_weight_is_valid(self):
        with self.client:
            self.assertTrue(ElectronicService.validate_weight(99))
            self.assertFalse(ElectronicService.validate_weight(-1))

    def test_if_ram_size_is_valid(self):
        with self.client:
            self.assertTrue(ElectronicService.validate_ram_size(8))
            self.assertTrue(ElectronicService.validate_ram_size(6))
            self.assertFalse(ElectronicService.validate_ram_size(-1))

    def test_if_cpu_cores_is_valid(self):
        with self.client:
            self.assertTrue(ElectronicService.validate_cpu_cores(4))
            self.assertTrue(ElectronicService.validate_cpu_cores(16))
            self.assertTrue(ElectronicService.validate_cpu_cores(7))
            self.assertFalse(ElectronicService.validate_cpu_cores(-4))

    def test_if_hd_size_is_valid(self):
        with self.client:
            self.assertTrue(ElectronicService.validate_hd_size(99))
            self.assertFalse(ElectronicService.validate_hd_size(-1))

    def test_create_desktop_object(self):
        with self.client:
            desktop = DesktopService.create_desktop('LG', 500, 100, 'intel', 32, 4, 20, '20x20')

            self.assertEqual(desktop.price, 500)
            self.assertEqual(desktop.weight, 100)
            self.assertEqual(desktop.brand, 'LG')
            self.assertEqual(desktop.processor, 'intel')
            self.assertEqual(desktop.ram_size, 32)
            self.assertEqual(desktop.cpu_cores, 4)
            self.assertEqual(desktop.hd_size, 20)
            self.assertEqual(desktop.dimensions, '20x20')

    def test_create_laptop_object(self):
        with self.client:
            laptop = LaptopService.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery', 'Windows 10', False, True)

            self.assertEqual(laptop.price, 600)
            self.assertEqual(laptop.weight, 200)
            self.assertEqual(laptop.brand, 'LG')
            self.assertEqual(laptop.display_size, '32x32')
            self.assertEqual(laptop.processor, 'intel')
            self.assertEqual(laptop.ram_size, 64)
            self.assertEqual(laptop.cpu_cores, 2)
            self.assertEqual(laptop.hd_size, 40)
            self.assertEqual(laptop.battery_info, 'Long lasting battery')
            self.assertEqual(laptop.os, 'Windows 10')
            self.assertEqual(laptop.touchscreen, False)
            self.assertEqual(laptop.camera, True)

    def test_create_tablet_object(self):
        with self.client:
            tablet = TabletService.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250, 'Long lasting battery', 'Windows 10', 'Good camera')

            self.assertEqual(tablet.price, 1200)
            self.assertEqual(tablet.weight, 1.2)
            self.assertEqual(tablet.brand, 'Microsoft')
            self.assertEqual(tablet.display_size, '10x12')
            self.assertEqual(tablet.dimensions, '10x12')
            self.assertEqual(tablet.processor, 'intel')
            self.assertEqual(tablet.ram_size, 8)
            self.assertEqual(tablet.cpu_cores, 2)
            self.assertEqual(tablet.hd_size, 250)
            self.assertEqual(tablet.battery, 'Long lasting battery')
            self.assertEqual(tablet.os, 'Windows 10')
            self.assertEqual(tablet.camera_info, 'Good camera')

    def test_create_monitor_object(self):
        with self.client:
            monitor = MonitorService.create_monitor('Asus', 300, 5, '25x30')

            self.assertEqual(monitor.price, 300)
            self.assertEqual(monitor.weight, 5)
            self.assertEqual(monitor.brand, 'Asus')
            self.assertEqual(monitor.dimensions, '25x30')

    def test_create_television_object(self):
        with self.client:
            television = TelevisionService.create_television('Panasonic', 3000, 15, 'Smart', '40x50')

            self.assertEqual(television.price, 3000)
            self.assertEqual(television.weight, 15)
            self.assertEqual(television.brand, 'Panasonic')
            self.assertEqual(television.type, 'Smart')
            self.assertEqual(television.dimensions, '40x50')

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
