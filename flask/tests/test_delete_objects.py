
import unittest
from tests.base_create_objects import BaseTestCase
from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.inventory_service import InventoryService
from project.models.inventory_model import Inventory
from project.orm import Mapper


# This class inherits from the base class in 'base_create_objects.py', in order to
# get the create_app, setUp and tearDown methods.
class TestDeletionObjects(BaseTestCase):

    def test_delete_desktop(self):
        with self.client:
            desktop = DesktopService.create_desktop('LG', 500, 100, 'intel', 32, 4, 20, '20x20')
            InventoryService.add_item_to_inventory(desktop.model)
            InventoryService.add_item_to_inventory(desktop.model)

            InventoryService.delete_item_from_inventory(desktop.model)
            rows = Mapper.query('inventories', model=desktop.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_laptop(self):
        with self.client:
            laptop = LaptopService.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery',
                                                 'Windows 10', False, True)
            InventoryService.add_item_to_inventory(laptop.model)
            InventoryService.add_item_to_inventory(laptop.model)

            InventoryService.delete_item_from_inventory(laptop.model)
            rows = Mapper.query('inventories', model=laptop.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_monitor(self):
        with self.client:
            monitor = MonitorService.create_monitor('Asus', 300, 5, '25x30')
            InventoryService.add_item_to_inventory(monitor.model)
            InventoryService.add_item_to_inventory(monitor.model)

            InventoryService.delete_item_from_inventory(monitor.model)
            rows = Mapper.query('inventories', model=monitor.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_tablet(self):
        with self.client:
            tablet = TabletService.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250,
                                                 'Long lasting battery', 'Windows 10', 'Good camera')
            InventoryService.add_item_to_inventory(tablet.model)
            InventoryService.add_item_to_inventory(tablet.model)

            InventoryService.delete_item_from_inventory(tablet.model)
            rows = Mapper.query('inventories', model=tablet.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
