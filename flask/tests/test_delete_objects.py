
import unittest
from tests.base_create_objects import BaseTestCase
from project.services.electronic_service import ElectronicService
from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.television_service import TelevisionService
from project.services.inventory_service import InventoryService
from project.gateaways.inventory_gateaway import InventoryGateaway
from project.services.unitofwork_service import UnitOfWorkService

# This class inherits from the base class in 'base_create_objects.py', in order to
# get the create_app, setUp and tearDown methods.
class TestDeletionObjects(BaseTestCase):

    def test_delete_desktop(self):
        unitofwork = UnitOfWorkService('new')
        with self.client:
            desktop = DesktopService.create_desktop('LG', 500, 100, 'intel', 32, 4, 20, '20x20')
            desktop1 = InventoryService.add_item_to_inventory(desktop.model)
            desktop2 = InventoryService.add_item_to_inventory(desktop.model)

            unitofwork.register_new('desktop', desktop)
            unitofwork.commit()
            unitofwork.register_new('inventory', desktop1)
            unitofwork.commit()
            unitofwork.register_new('inventory', desktop2)
            unitofwork.commit()

            InventoryService.delete_item_from_inventory(desktop.model)
            rows = InventoryGateaway.query_filtered_by(model=desktop.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1,len(items))

    def test_delete_laptop(self):
        unitofwork = UnitOfWorkService('new')
        with self.client:
            laptop = LaptopService.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery',
                                                 'Windows 10', False, True)
            laptop1 = InventoryService.add_item_to_inventory(laptop.model)
            laptop2 = InventoryService.add_item_to_inventory(laptop.model)

            unitofwork.register_new('laptop', laptop)
            unitofwork.commit()
            unitofwork.register_new('inventory', laptop1)
            unitofwork.commit()
            unitofwork.register_new('inventory', laptop2)
            unitofwork.commit()

            InventoryService.delete_item_from_inventory(laptop.model)
            rows = InventoryGateaway.query_filtered_by(model=laptop.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_monitor(self):
        unitofwork = UnitOfWorkService('new')
        with self.client:
            monitor = MonitorService.create_monitor('Asus', 300, 5, '25x30')
            monitor1 = InventoryService.add_item_to_inventory(monitor.model)
            monitor2 = InventoryService.add_item_to_inventory(monitor.model)

            unitofwork.register_new('monitor', monitor)
            unitofwork.commit()
            unitofwork.register_new('inventory', monitor1)
            unitofwork.commit()
            unitofwork.register_new('inventory', monitor2)
            unitofwork.commit()

            InventoryService.delete_item_from_inventory(monitor.model)
            rows = InventoryGateaway.query_filtered_by(model=monitor.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_tablet(self):
        unitofwork = UnitOfWorkService('new')
        with self.client:
            tablet = TabletService.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250,
                                                 'Long lasting battery', 'Windows 10', 'Good camera')
            tablet1 = InventoryService.add_item_to_inventory(tablet.model)
            tablet2 = InventoryService.add_item_to_inventory(tablet.model)

            unitofwork.register_new('tablet', tablet)
            unitofwork.commit()
            unitofwork.register_new('inventory', tablet1)
            unitofwork.commit()
            unitofwork.register_new('inventory', tablet2)
            unitofwork.commit()

            InventoryService.delete_item_from_inventory(tablet.model)
            rows = InventoryGateaway.query_filtered_by(model=tablet.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

    def test_delete_television(self):
        unitofwork = UnitOfWorkService('new')
        with self.client:
            television = TelevisionService.create_television('Panasonic', 3000, 15, 'Smart', '40x50')
            television1 = InventoryService.add_item_to_inventory(television.model)
            television2 = InventoryService.add_item_to_inventory(television.model)

            unitofwork.register_new('television', television)
            unitofwork.commit()
            unitofwork.register_new('inventory', television1)
            unitofwork.commit()
            unitofwork.register_new('inventory', television2)
            unitofwork.commit()

            InventoryService.delete_item_from_inventory(television.model)
            rows = InventoryGateaway.query_filtered_by(model=television.model)
            items = InventoryService.get_inventory_items_from_rows(rows)
            self.assertEqual(1, len(items))

# Runs the tests.
if __name__ == '__main__':
    unittest.main()



