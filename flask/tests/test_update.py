

import unittest
from tests.base_create_objects import BaseTestCase
from project.controllers.electronic import ElectronicController
from project.controllers.desktop import DesktopController
from project.controllers.laptop import LaptopController
from project.controllers.monitor import MonitorController
from project.controllers.tablet import TabletController
from project.controllers.inventory import InventoryController
from project.orm import Mapper


# This class inherits from the base class in 'base_create_objects.py', in order to
# get the create_app, setUp and tearDown methods.
class TestUpdateObjects(BaseTestCase):

    def test_update_desktop(self):
        with self.client:
            desktop1 = DesktopController.create_desktop('Asus', 500, 100, 'intel', 32, 4, 20, '20x20')
            desktop2 = DesktopController.create_desktop('LG', 500, 100, 'intel', 32, 4, 20, '20x20')
            DesktopController.update_desktop(desktop1.model,brand='Apple', price=600, weight=100, processor='intel', ram_size=32, cpu_cores=4, hd_size=20, dimensions='20x20' )
            rows = Mapper.query('desktops',model=desktop1.model)
            desktop= DesktopController.get_desktops_from_rows(rows)[0]

            self.assertEqual(desktop.model, desktop1.model)
            self.assertEqual(desktop.brand, 'Apple')
            self.assertEqual(desktop.price, 600)


    def test_update_laptop(self):
        with self.client:
            laptop1 = LaptopController.create_laptop('LG', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery', 'Windows 10', False, True)
            laptop2 = LaptopController.create_laptop('Asus', 600, 200, '32x32', 'intel', 64, 2, 40, 'Long lasting battery', 'Windows 10', False, True)
            LaptopController.update_laptop(laptop1.model, brand='Apple', price=1200, weight=400, display_size='30x30', processor='intel',
                                        ram_size=64, cpu_cores=2, hd_size=40, battery_info='Long lasting battery', os='Windows 10',
                                        touchscreen=False, camera=True)

            rows = Mapper.query('laptops', model=laptop1.model)
            laptop = LaptopController.get_laptops_from_rows(rows)[0]

            self.assertEqual(laptop.model, laptop1.model)
            self.assertEqual(laptop.brand, 'Apple')
            self.assertEqual(laptop.price, 1200)
            self.assertEqual(laptop.weight, 400)
            self.assertEqual(laptop.processor, 'intel')

    def test_update_monitor(self):
        with self.client:
            monitor1 = MonitorController.create_monitor('Asus', 300, 5, '25x30')
            monitor2 = MonitorController.create_monitor('Apple', 300, 5, '25x30')
            MonitorController.update_monitor(monitor1.model, brand='LG', price=500, weight=50, dimensions='30x30')
            rows= Mapper.query('monitors', model=monitor1.model)
            monitor= MonitorController.get_monitors_from_rows(rows)[0]

            self.assertEqual(monitor.price, 500)
            self.assertEqual(monitor.model, monitor1.model)
            self.assertEqual(monitor.weight, 50)
            self.assertEqual(monitor.brand, 'LG')
            self.assertEqual(monitor.dimensions, '30x30')

    def test_update_tablet(self):
        with self.client:
            tablet1 = TabletController.create_tablet('Microsoft', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250, 'Long lasting battery', 'Windows 10', 'Good camera')
            tablet2 = TabletController.create_tablet('Samsung', 1200, 1.2, '10x12', '10x12', 'intel', 8, 2, 250, 'Long lasting battery', 'Windows 10', 'Good camera')
            TabletController.update_tablet(tablet1.model, brand='Apple', price=1800, weight=10, display_size='12x12', dimensions='10x10',
                                        processor='AMD', ram_size=16, cpu_cores=4, hd_size=350, battery='Short lasting battery',
                                        os='Windows 11', camera_info='Meh camera')
            rows = Mapper.query('tablets', model=tablet1.model)
            tablet = TabletController.get_tablets_from_rows(rows)[0]

            self.assertEqual(tablet.model, tablet1.model)
            self.assertEqual(tablet.price, 1800)
            self.assertEqual(tablet.weight, 10)
            self.assertEqual(tablet.brand, 'Apple')
            self.assertEqual(tablet.display_size, '12x12')
            self.assertEqual(tablet.dimensions, '10x10')
            self.assertEqual(tablet.processor, 'AMD')
            self.assertEqual(tablet.ram_size, 16)
            self.assertEqual(tablet.cpu_cores, 4)
            self.assertEqual(tablet.hd_size, 350)
            self.assertEqual(tablet.battery, 'Short lasting battery')
            self.assertEqual(tablet.os, 'Windows 11')
            self.assertEqual(tablet.camera_info, 'Meh camera')


# Runs the tests.
if __name__ == '__main__':
    unittest.main()