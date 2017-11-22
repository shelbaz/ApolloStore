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
from tests.base_viewmodels import BaseTestCase
from project.controllers.desktop import DesktopController
from project.controllers.tablet import TabletController
from project.controllers.monitor import MonitorController
from project.controllers.laptop import LaptopController
from project.controllers.inventory import InventoryController
from project.controllers.cart import CartController
from project.controllers.authentication import AuthenticationController
from project.controllers.purchase import PurchaseController
from project.orm import Mapper


# This class inherits from the base class in 'base_viewmodels.py', in order to
# get the create_app, setUp and tearDown methods.
class TestViewModels(BaseTestCase):
    
    # Test to see if the query function works for the Laptop class
    def test_should_return_query_results_for_laptop(self):
        with self.client:
            LaptopController.create_laptop('Asus', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', True, True)
            LaptopController.create_laptop('Lenovo', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)
            LaptopController.create_laptop('Dell', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)

            rows1 = Mapper.query('items', 'laptops', brand='Asus')
            rows2 = Mapper.query('items', 'laptops', brand='Acer')
            result1= LaptopController.get_laptops_from_rows(rows1)
            result2= LaptopController.get_laptops_from_rows(rows2)
            self.assertEqual(result1[0].brand, 'Asus')
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Tablet class
    def test_should_return_query_results_for_tablet(self):
        with self.client:
            TabletController.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletController.create_tablet('Dell', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletController.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')

            rows1 = Mapper.query('items', 'tablets', brand='Asus')
            rows2 = Mapper.query('items', 'tablets', brand='Apple')
            result1 = TabletController.get_tablets_from_rows(rows1)
            result2 = TabletController.get_tablets_from_rows(rows2)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Tablet class

    # Test to see if the query function works for the Desktop class
    def test_should_return_query_results_for_desktop(self):
        with self.client:
            DesktopController.create_desktop('Asus', 600, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopController.create_desktop('Dell', 500, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopController.create_desktop('Lenovo', 500, 10, 'intel', 256, 2, 1080, '100x100')

            rows1 = Mapper.query('items', 'desktops', brand='Asus')
            rows2 = Mapper.query('items', 'desktops', brand='Acer')
            result1 = DesktopController.get_desktops_from_rows(rows1)
            result2 = DesktopController.get_desktops_from_rows(rows2)
            self.assertEqual(result1[0].price, 600)
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Monitor class
    def test_should_return_query_results_for_monitor(self):
        with self.client:
            MonitorController.create_monitor('Asus', 600, 10, '125x100')
            MonitorController.create_monitor('Dell', 600, 10, '150x100')
            MonitorController.create_monitor('Asus', 600, 10, '170x100')

            rows1 = Mapper.query('items', 'monitors', dimensions='150x100')
            rows2 = Mapper.query('items', 'monitors', brand='Acer')
            result1 = MonitorController.get_monitors_from_rows(rows1)
            result2 = MonitorController.get_monitors_from_rows(rows2)
            self.assertEqual(result1[0].brand, 'Dell')
            self.assertEqual(result2, None)

    # Tests to see if all desktops will be returned
    def test_should_return_all_desktops(self):
        with self.client:

            result = DesktopController.get_all_desktops()
            self.assertEqual(result, None)

            DesktopController.create_desktop('Asus', 600, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopController.create_desktop('Dell', 500, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopController.create_desktop('Lenovo', 500, 10, 'intel', 256, 2, 1080, '100x100')

            result = DesktopController.get_all_desktops()
            self.assertEqual(len(result), 3)

    # Tests to see if all laptops will be returned
    def test_should_return_all_laptops(self):
        with self.client:
            result = LaptopController.get_all_laptops()
            self.assertEqual(result, None)

            LaptopController.create_laptop('Asus', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', True, True)
            LaptopController.create_laptop('Lenovo', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)
            LaptopController.create_laptop('Dell', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)

            result = LaptopController.get_all_laptops()
            self.assertEqual(len(result), 3)

    # Tests to see if all tablets will be returned
    def test_should_return_all_tablets(self):
        with self.client:
            result = TabletController.get_all_tablets()
            self.assertEqual(result, None)

            TabletController.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletController.create_tablet('Dell', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletController.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')

            result = TabletController.get_all_tablets()
            self.assertEqual(len(result), 3)

    # Tests to see if all monitors will be returned
    def test_should_return_all_monitors(self):
        with self.client:
            result = MonitorController.get_all_monitors()
            self.assertEqual(result, None)

            MonitorController.create_monitor('Asus', 600, 10, '125x100')
            MonitorController.create_monitor('Dell', 600, 10, '150x100')

            result = MonitorController.get_all_monitors()
            self.assertEqual(len(result), 2)

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
