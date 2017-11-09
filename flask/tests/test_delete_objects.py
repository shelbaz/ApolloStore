
import unittest
from tests.base_create_objects import BaseTestCase
from project.controllers.desktop import DesktopController
from project.controllers.laptop import LaptopController
from project.controllers.monitor import MonitorController
from project.controllers.tablet import TabletController
from project.controllers.inventory import InventoryController
from project.orm import Mapper


# This class inherits from the base class in 'base_create_objects.py', in order to
# get the create_app, setUp and tearDown methods.
class TestDeletionObjects(BaseTestCase):

    def test_delete_desktop(self):
        with self.client:
            desktop = DesktopController.create_desktop('LG', 500, 100, 'intel', 32, 4, 20, '20x20')
            rows = Mapper.query('inventories', model=desktop.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(items, None)
            InventoryController.delete_item_from_inventory(desktop.model)
            InventoryController.add_item_to_inventory(desktop.model, desktop.__class__.__name__)
            InventoryController.add_item_to_inventory(desktop.model, desktop.__class__.__name__)
            InventoryController.delete_item_from_inventory(desktop.model)
            rows = Mapper.query('inventories', model=desktop.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_laptop(self):
        with self.client:
            laptop = LaptopController.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery',
                                                 'Windows 10', False, True)
            rows = Mapper.query('inventories', model=laptop.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(items, None)
            InventoryController.delete_item_from_inventory(laptop.model)
            InventoryController.add_item_to_inventory(laptop.model, laptop.__class__.__name__)
            InventoryController.add_item_to_inventory(laptop.model, laptop.__class__.__name__)

            InventoryController.delete_item_from_inventory(laptop.model)
            rows = Mapper.query('inventories', model=laptop.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_monitor(self):
        with self.client:
            monitor = MonitorController.create_monitor('Asus', 300, 5, '25x30')
            rows = Mapper.query('inventories', model=monitor.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(items, None)
            InventoryController.delete_item_from_inventory(monitor.model)
            InventoryController.add_item_to_inventory(monitor.model, monitor.__class__.__name__)
            InventoryController.add_item_to_inventory(monitor.model, monitor.__class__.__name__)

            InventoryController.delete_item_from_inventory(monitor.model)
            rows = Mapper.query('inventories', model=monitor.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_tablet(self):
        with self.client:
            tablet = TabletController.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250,
                                                 'Long lasting battery', 'Windows 10', 'Good camera')
            rows = Mapper.query('inventories', model=tablet.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(items, None)
            InventoryController.delete_item_from_inventory(tablet.model)
            InventoryController.add_item_to_inventory(tablet.model, tablet.__class__.__name__)
            InventoryController.add_item_to_inventory(tablet.model, tablet.__class__.__name__)

            InventoryController.delete_item_from_inventory(tablet.model)
            rows = Mapper.query('inventories', model=tablet.model)
            items = InventoryController.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
