from project.services.desktop_service import delete_desktop
from project.services.laptop_service import delete_laptop
from project.services.monitor_service import delete_monitor
from project.services.tablet_service import delete_tablet
from project.services.television_service import delete_television

def delete_electronic(type):
    if type == 'desktops':
        delete_desktop()
    elif type == 'laptops':
        delete_laptop()
    elif type == 'monitors':
        delete_monitor()
    elif type == 'tablets':
        delete_tablet()
    elif type == 'televisions':
        delete_television()
    else:
        return