
import unittest
from tests.base_create_objects import BaseTestCase
from project.services.electronic_service import ElectronicService
from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.television_service import TelevisionService
from project.services.inventory_service import InventoryService
from project.gateways.inventory_gateway import InventoryGateway


# This class inherits from the base class in 'base_create_objects.py', in order to
# get the create_app, setUp and tearDown methods.
class TestDeletionObjects(BaseTestCase):

    def test_delete_desktop(self):
        with self.client:
            desktop = DesktopService.create_desktop('LG', 500, 100, 'intel', 32, 4, 20, '20x20')
            InventoryService.add_item_to_inventory(desktop.model)
            InventoryService.add_item_to_inventory(desktop.model)

            InventoryService.delete_electronic(desktop.model)
            rows = InventoryGateway.query_filtered_by(model=desktop.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1,len(items))

    def test_delete_laptop(self):
        with self.client:
            laptop = LaptopService.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery',
                                                 'Windows 10', False, True)
            InventoryService.add_item_to_inventory(laptop.model)
            InventoryService.add_item_to_inventory(laptop.model)

            InventoryService.delete_electronic(laptop.model)
            rows = InventoryGateway.query_filtered_by(model=laptop.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_monitor(self):
        with self.client:
            monitor = MonitorService.create_monitor('Asus', 300, 5, '25x30')
            InventoryService.add_item_to_inventory(monitor.model)
            InventoryService.add_item_to_inventory(monitor.model)

            InventoryService.delete_electronic(monitor.model)
            rows = InventoryGateway.query_filtered_by(model=monitor.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_tablet(self):
        with self.client:
            tablet = TabletService.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250,
                                                 'Long lasting battery', 'Windows 10', 'Good camera')
            InventoryService.add_item_to_inventory(tablet.model)
            InventoryService.add_item_to_inventory(tablet.model)

            InventoryService.delete_electronic(tablet.model)
            rows = InventoryGateway.query_filtered_by(model=tablet.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_television(self):
        with self.client:
            television = TelevisionService.create_television('Panasonic', 3000, 15, 'Smart', '40x50')
            InventoryService.add_item_to_inventory(television.model)
            InventoryService.add_item_to_inventory(television.model)

            InventoryService.delete_electronic(television.model)
            rows = InventoryGateway.query_filtered_by(model=television.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

# Runs the tests.
if __name__ == '__main__':
    unittest.main()



