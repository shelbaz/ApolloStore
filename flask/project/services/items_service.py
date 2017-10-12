from project.services.desktop_service import DesktopService
from project.services.laptop_service import LaptopService
from project.services.monitor_service import MonitorService
from project.services.tablet_service import TabletService
from project.services.television_service import TelevisionService
from project.services.inventory_service import InventoryService

def delete_electronic(type, item):
    if type == 'desktops':
        DesktopService.delete_desktop(item)
    elif type == 'laptops':
        LaptopService.delete_laptop(item)
    elif type == 'monitors':
        MonitorService.delete_monitor(item)
    elif type == 'tablets':
        TabletService.delete_tablet(item)
    elif type == 'televisions':
        TelevisionService.delete_television(item)
    elif type == 'inventories':
        InventoryService.delete_item_from_inventory(item)
    else:
        return

