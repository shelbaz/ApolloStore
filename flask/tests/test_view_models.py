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
from project.services.television_service import TelevisionService
from project.services.tablet_service import TabletService
from project.services.monitor_service import MonitorService
from project.services.laptop_service import LaptopService
from project.models.desktop_model import Desktop
from project.models.laptop_model import Laptop
from project.models.monitor_model import Monitor
from project.models.tablet_model import Tablet
from project.models.television_model import Television
from project.models.inventory_model import Inventory
from project.services.electronic_service import ElectronicService
from project.services.inventory_service import InventoryService
from project.gateways import get_inventory_count


# This class inherits from the base class in 'base_viewmodels.py', in order to
# get the create_app, setUp and tearDown methods.
class TestViewModels(BaseTestCase):
    # Test to see if the query function works for the Laptop class
    def test_should_return_query_results_for_laptop(self):
        with self.client:
            LaptopService.create_laptop('Asus', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', True, True)
            LaptopService.create_laptop('Lenovo', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)
            LaptopService.create_laptop('Dell', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)

            rows1 = Laptop.query(brand='Asus')
            rows2 = Laptop.query(brand='Acer')
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

            rows1 = Tablet.query(brand='Asus')
            rows2 = Tablet.query(brand='Apple')
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

            rows1 = Desktop.query(brand='Asus')
            rows2 = Desktop.query(brand='Acer')
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

            rows1 = Monitor.query(dimensions='150x100')
            rows2 = Monitor.query(brand='Acer')
            result1 = MonitorService.get_monitors_from_rows(rows1)
            result2 = MonitorService.get_monitors_from_rows(rows2)
            self.assertEqual(result1[0].brand, 'Dell')
            self.assertEqual(result2, None)

    # Test to see if the query function works for the Television class
    def test_should_return_query_results_for_television(self):
        with self.client:
            TelevisionService.create_television('Asus', 600, 10, 'HD', '125x100')
            TelevisionService.create_television('Asus', 600, 10, 'LED', '125x100')
            TelevisionService.create_television('Samsung', 600, 10, '3D', '125x100')
            TelevisionService.create_television('Asus', 600, 10, 'Smart', '125x100')

            rows1 = Television.query(type='3D')
            rows2 = Television.query(brand='Toshiba')
            result1 = TelevisionService.get_televisions_from_rows(rows1)
            result2 = TelevisionService.get_televisions_from_rows(rows2)
            self.assertEqual(result1[0].brand, 'Samsung')
            self.assertEqual(result2, None)

    # Test to see if get_inventory_count function works for Electronics
    def test_should_count_for_searched_model(self):
        with self.client:
            tv1 = TelevisionService.create_television('Asus', 600, 10, 'HD', '125x100')
            result = get_inventory_count('televisions', tv1.model)
            self.assertEqual(result, 0)
            InventoryService.add_item_to_inventory(tv1.model)
            result = get_inventory_count('televisions', tv1.model)
            self.assertEqual(result, 1)

    # Test to see if add item to inventory works for Electronics
    def test_should_add_item_to_inventory(self):
        with self.client:
            tv1 = TelevisionService.create_television('Asus', 600, 10, 'HD', '125x100')
            InventoryService.add_item_to_inventory(tv1.model)
            InventoryService.add_item_to_inventory(tv1.model)
            rows = Inventory.query(model=tv1.model)
            result = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(len(result), 2)

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

    # Tests to see if all televisions will be returned
    def test_should_return_all_televisions(self):
        with self.client:
            result = TelevisionService.get_all_televisions()
            self.assertEqual(result, None)

            TelevisionService.create_television('Asus', 600, 10, 'HD', '125x100')
            TelevisionService.create_television('Asus', 600, 10, 'LED', '125x100')
            TelevisionService.create_television('Samsung', 600, 10, '3D', '125x100')
            TelevisionService.create_television('Asus', 600, 10, 'Smart', '125x100')

            result = TelevisionService.get_all_televisions()
            self.assertEqual(len(result), 4)

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
