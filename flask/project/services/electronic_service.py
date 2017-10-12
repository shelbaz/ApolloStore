
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.desktop_model import Desktop
from project.models.laptop_model import Laptop
from project.models.monitor_model import Monitor
from project.models.tablet_model import Tablet
from project.models.television_model import Television
from project.models.inventory_model import Inventory
from project.models.item_model import Item
from project.gateaways.inventory_gateaway import InventoryGateaway
from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.television_service import TelevisionService
from re import match
from uuid import uuid4
import traceback


class ElectronicService():

    # Validates that a positive price is entered
    @staticmethod
    def validate_price(price):
        return (float(price) > 0)

    # Validates that a positive weight is entered
    @staticmethod
    def validate_weight(weight):
        return (float(weight) > 0)

    # Validates that the RAM size entered is greater than 0
    @staticmethod
    def validate_ram_size(ram_size):
        return (int(ram_size) > 0)

    @staticmethod
    def validate_cpu_cores(cpu_cores):
        return (int(cpu_cores) > 0)

    # Validates that a positive hard drive disk size is entered
    @staticmethod
    def validate_hd_size(hd_size):
        return (int(hd_size) > 0)

    # Deletes an item
    def delete_electronic(type):
        if type == 'desktops':
            DesktopService.delete_desktop()
        elif type == 'laptops':
            LaptopService.delete_laptop()
        elif type == 'monitors':
            MonitorService.delete_monitor()
        elif type == 'tablets':
            TabletService.delete_tablet()
        elif type == 'televisions':
            TelevisionService.delete_television()
        else:
            return

