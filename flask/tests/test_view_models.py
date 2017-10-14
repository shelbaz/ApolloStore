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
from project.services.desktop_service import DesktopService
from project.services.tablet_service import TabletService
from project.services.monitor_service import MonitorService
from project.services.laptop_service import LaptopService
from project.models.desktop_model import Desktop
from project.models.laptop_model import Laptop
from project.models.monitor_model import Monitor
from project.models.tablet_model import Tablet
from project.models.inventory_model import Inventory
from project.services.inventory_service import InventoryService
from project.gateways import get_inventory_count
from project.orm import Mapper


# This class inherits from the base class in 'base_viewmodels.py', in order to
# get the create_app, setUp and tearDown methods.
class TestViewModels(BaseTestCase):
    
    # Test to see if the query function works for the Laptop class
    def test_should_return_query_results_for_laptop(self):
        with self.client:
            LaptopService.create_laptop('Asus', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', True, True)
            LaptopService.create_laptop('Lenovo', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)
            LaptopService.create_laptop('Dell', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)

            rows1 = Mapper.query('items', 'laptops', brand='Asus')
            rows2 = Mapper.query('items', 'laptops', brand='Acer')
            result1= LaptopService.get_laptops_from_rows(rows1)
            result2= LaptopService.get_laptops_from_rows(rows2)
            self.assertEqual(result1[0].brand, 'Asus')
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Tablet class
    def test_should_return_query_results_for_tablet(self):
        with self.client:
            TabletService.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletService.create_tablet('Dell', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletService.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')

            rows1 = Mapper.query('items', 'tablets', brand='Asus')
            rows2 = Mapper.query('items', 'tablets', brand='Apple')
            result1 = TabletService.get_tablets_from_rows(rows1)
            result2 = TabletService.get_tablets_from_rows(rows2)
            self.assertEqual(len(result1), 2)
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Desktop class
    def test_should_return_query_results_for_desktop(self):
        with self.client:
            DesktopService.create_desktop('Asus', 600, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopService.create_desktop('Dell', 500, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopService.create_desktop('Lenovo', 500, 10, 'intel', 256, 2, 1080, '100x100')

            rows1 = Mapper.query('items', 'desktops', brand='Asus')
            rows2 = Mapper.query('items', 'desktops', brand='Acer')
            result1 = DesktopService.get_desktops_from_rows(rows1)
            result2 = DesktopService.get_desktops_from_rows(rows2)
            self.assertEqual(result1[0].price, 600)
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Monitor class
    def test_should_return_query_results_for_monitor(self):
        with self.client:
            MonitorService.create_monitor('Asus', 600, 10, '125x100')
            MonitorService.create_monitor('Dell', 600, 10, '150x100')
            MonitorService.create_monitor('Asus', 600, 10, '170x100')

            rows1 = Mapper.query('items', 'monitors', dimensions='150x100')
            rows2 = Mapper.query('items', 'monitors', brand='Acer')
            result1 = MonitorService.get_monitors_from_rows(rows1)
            result2 = MonitorService.get_monitors_from_rows(rows2)
            self.assertEqual(result1[0].brand, 'Dell')
            self.assertEqual(result2, None)

    # Tests to see if all desktops will be returned
    def test_should_return_all_desktops(self):
        with self.client:

            result = DesktopService.get_all_desktops()
            self.assertEqual(result, None)

            DesktopService.create_desktop('Asus', 600, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopService.create_desktop('Dell', 500, 10, 'intel', 256, 2, 1080, '100x100')
            DesktopService.create_desktop('Lenovo', 500, 10, 'intel', 256, 2, 1080, '100x100')

            result = DesktopService.get_all_desktops()
            self.assertEqual(len(result), 3)

    # Tests to see if all laptops will be returned
    def test_should_return_all_laptops(self):
        with self.client:
            result = LaptopService.get_all_laptops()
            self.assertEqual(result, None)

            LaptopService.create_laptop('Asus', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', True, True)
            LaptopService.create_laptop('Lenovo', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)
            LaptopService.create_laptop('Dell', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)

            result = LaptopService.get_all_laptops()
            self.assertEqual(len(result), 3)

    # Tests to see if all tablets will be returned
    def test_should_return_all_tablets(self):
        with self.client:
            result = TabletService.get_all_tablets()
            self.assertEqual(result, None)

            TabletService.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletService.create_tablet('Dell', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            TabletService.create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')

            result = TabletService.get_all_tablets()
            self.assertEqual(len(result), 3)

    # Tests to see if all monitors will be returned
    def test_should_return_all_monitors(self):
        with self.client:
            result = MonitorService.get_all_monitors()
            self.assertEqual(result, None)

            MonitorService.create_monitor('Asus', 600, 10, '125x100')
            MonitorService.create_monitor('Dell', 600, 10, '150x100')

            result = MonitorService.get_all_monitors()
            self.assertEqual(len(result), 2)

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
