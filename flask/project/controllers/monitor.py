
from project import logger
from project.models.monitor import Monitor
from project.gateways import get_inventory_count
from project.controllers.electronic import ElectronicController
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from project.orm import Mapper


class MonitorController():

    identityMap = IdentityMap()

    # Creates a monitor that is valid
    @staticmethod
    def create_monitor(brand, price, weight, dimensions):
        try:
            if ElectronicController.validate_price(price) and ElectronicController.validate_weight(weight):
                monitor = Monitor(model=str(uuid4()), brand=brand, price=price, weight=weight, dimensions=dimensions)
                monitor.insert()
                MonitorController.identityMap.set(monitor.model, monitor)

                logger.info('Monitor created successfully!')

                return monitor

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def update_monitor(model, **conditions):
        rows = Mapper.query('monitors', model=model)
        monitor = MonitorController.get_monitors_from_rows(rows)[0]
        monitor.update(**conditions)

    # Queries the list of all monitors and their count
    @staticmethod
    def get_all_monitors():
        try:
            rows = Mapper.query('items', 'monitors')
            monitors = MonitorController.get_monitors_from_rows(rows)
            monitors_with_count = []

            if monitors:
                for monitor in monitors:
                    count = get_inventory_count('monitors', monitor.model)
                    monitors_with_count.append([monitor, count])
                return monitors_with_count
            else:
                return None
        except Exception:
            logger.error(traceback.format_exc())

    # Returns all monitors from rows taken from db
    @staticmethod
    def get_monitors_from_rows(rows):
        if rows:
            monitors = []
            for row in rows:
                #check identity map
                if MonitorController.identityMap.hasId(row[0]):
                    monitor = MonitorController.identityMap.getObject(row[0])
                else:
                    monitor = Monitor(row[0], row[1], row[2], row[3], row[4])
                    MonitorController.identityMap.set(monitor.model, monitor)

                monitors.append(monitor)
            
            if monitors:
                return monitors
            else:
                return None
        else:
            return None

    @staticmethod
    def delete_model(model):
        try:
            rows = Mapper.query('items', 'monitors', model=model)
            monitor = MonitorController.get_monitors_from_rows(rows)[0]

            monitor.delete()

        except Exception:
            logger.error(traceback.format_exc())
