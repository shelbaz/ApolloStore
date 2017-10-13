from flask import g
from project import logger
from re import match
from uuid import uuid4
from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.television_service import TelevisionService
from project.services.inventory_service import InventoryService

import traceback

class UnitOfWorkService():

    def __init__(self, type_action):

        # Initializes object attributes
        self.type_action = type_action
        self.type_electronic = ''
        self.item = ''


    def register_dirty(self, type_electronic, item):
        self.type_electronic = type_electronic
        self.item = item

    def register_deleted(self, type_electronic, item):
        self.type_electronic = type_electronic
        self.item = item

    def register_new(self, type_electronic, item):
        self.type_electronic = type_electronic
        self.item = item

    def commit(self):
        if (self.type_action == 'new'):
            UnitOfWorkService.create_item(self)
        elif (self.type_action == 'update'):
            UnitOfWorkService.update_item()
        elif(self.type_action == 'delete'):
            UnitOfWorkService.delete_item()
        else:
            return


    def create_item(self):
        if (self.type_electronic == 'desktop'):
            DesktopService.insert_desktop(self.item)
        elif (self.type_electronic == 'laptop'):
            LaptopService.insert_laptop(self.item)
        elif (self.type_electronic == 'monitor'):
            MonitorService.insert_monitor(self.item)
        elif (self.type_electronic == 'tablet'):
            TabletService.insert_tablet(self.item)
        elif (self.type_electronic == 'television'):
            TelevisionService.insert_television(self.item)
        else:
            InventoryService.insert_inventory(self.item)

    # def update_item(self):
    #     if (self.type_electronic == 'desktops'):
    #         DesktopService.update_desktop(self.item)
    #     elif (self.type_electronic == 'laptops'):
    #         LaptopService.update_laptop(self.item)
    #     elif (self.type_electronic == 'monitors'):
    #         MonitorService.update_monitor(self.item)
    #     elif (self.type_electronic == 'tablets'):
    #         TabletService.update_tablet(self.item)
    #     elif (self.type_electronic == 'television'):
    #         TelevisionService.update_television(self.item)
    #     else:
    #         return
    #
    # def delete_item(self):
    #     if (self.type_electronic == 'desktops'):
    #         DesktopService.delete_desktop(self.item)
    #     elif (self.type_electronic == 'laptops'):
    #         LaptopService.delete_laptop(self.item)
    #     elif (self.type_electronic == 'monitors'):
    #         MonitorService.delete_monitor(self.item)
    #     elif (self.type_electronic == 'tablets'):
    #         TabletService.delete_tablet(self.item)
    #     elif (self.type_electronic == 'television'):
    #         TelevisionService.delete_television(self.item)
    #     else:
    #         return
