
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
            self.assertEqual(items, None)

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
            self.assertEqual(items, None)

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
            self.assertEqual(items, None)

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
            self.assertEqual(items, None)

    # Test to see if the desktop specification is set to hidden when it is deleted
    def test_should_delete_desktop_spec(self):
        with self.client:
            desktop = DesktopController.create_desktop('Asus', 600, 10, 'intel', 256, 2, 1080, '100x100')
            InventoryController.add_item_to_inventory(desktop.model, 'desktops')
            DesktopController.delete_model(desktop.model)
            rows = Mapper.query('desktops', model=desktop.model)
            desktop = DesktopController.get_desktops_from_rows(rows)[0]
            self.assertEqual(desktop.hide, True)

    # Test to see if the laptop specification is set to hidden when it is deleted
    def test_should_delete_laptop_spec(self):
        with self.client:
            laptop = LaptopController.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery',
                                                 'Windows 10', False, True)
            InventoryController.add_item_to_inventory(laptop.model, 'laptops')
            LaptopController.delete_model(laptop.model)
            rows = Mapper.query('laptops', model=laptop.model)
            laptop = LaptopController.get_laptops_from_rows(rows)[0]
            self.assertEqual(laptop.hide, True)

    # Test to see if the tablet specification is set to hidden when it is deleted
    def test_should_delete_tablet_spec(self):
        with self.client:
            tablet = TabletController.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250,
                                                    'Long lasting battery', 'Windows 10', 'Good camera')
            InventoryController.add_item_to_inventory(tablet.model, 'tablets')
            TabletController.delete_model(tablet.model)
            rows = Mapper.query('tablets', model=tablet.model)
            tablet = TabletController.get_tablets_from_rows(rows)[0]
            self.assertEqual(tablet.hide, True)

    # Test to see if the monitor specification is set to hidden when it is deleted
    def test_should_delete_monitor_spec(self):
        with self.client:
            monitor = MonitorController.create_monitor('Asus', 300, 5, '25x30')
            InventoryController.add_item_to_inventory(monitor.model, 'monitors')
            MonitorController.delete_model(monitor.model)
            rows = Mapper.query('monitors', model=monitor.model)
            monitor = MonitorController.get_monitors_from_rows(rows)[0]
            self.assertEqual(monitor.hide, True)


# Runs the tests.
if __name__ == '__main__':
    unittest.main()
