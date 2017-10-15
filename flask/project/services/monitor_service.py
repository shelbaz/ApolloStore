
from project import logger
from project.models.monitor_model import Monitor
from project.gateways import get_inventory_count
from project.services.electronic_service import ElectronicService
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from project.orm import Mapper


class MonitorService():

    identityMap = IdentityMap()

    # Creates a monitor that is valid
    @staticmethod
    def create_monitor(brand, price, weight, dimensions):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight):
                monitor = Monitor(model=str(uuid4()), brand=brand, price=price, weight=weight, dimensions=dimensions)
                monitor.insert()
                MonitorService.identityMap.set(monitor.model, monitor)

                logger.info('Monitor created successfully!')

                return monitor

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def update_monitor(model, brand, price, weight, dimensions):
        try:
            rows = MonitorGateaway.query_filtered_by(model=model)
            monitor1 = MonitorService.get_monitors_from_rows(rows)[0]
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight):
                monitor2 = Monitor(model=str(uuid4()), brand=brand, price=price, weight=weight, dimensions=dimensions)
                MonitorGateaway.remove_from_db(monitor1)
                ItemGateaway.remove_from_db(monitor1)
                ItemGateaway.insert_into_db(monitor2)
                MonitorGateaway.insert_into_db(monitor2)
                MonitorService.identityMap.set(monitor2.model, monitor2)

                logger.info('Monitor updated successfully!')

                return monitor2
        except Exception as e:
            logger.error(traceback.format_exc())

    # Queries the list of all monitors and their count
    @staticmethod
    def get_all_monitors():
        try:
            rows = Mapper.query('items', 'monitors')
            monitors = MonitorService.get_monitors_from_rows(rows)
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
                if MonitorService.identityMap.hasId(row[0]):
                    monitor = MonitorService.identityMap.getObject(row[0])
                else:
                    monitor = Monitor(row[0], row[1], row[2], row[3], row[4])
                    MonitorService.identityMap.set(monitor.model, monitor)

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
            monitor = MonitorService.get_monitors_from_rows(rows)[0]

            monitor.delete()

        except Exception:
            logger.error(traceback.format_exc())
