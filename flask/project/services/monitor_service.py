
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.monitor_model import Monitor
from project.gateaways import delete_item
from project.gateaways.monitor_gateaway import MonitorGateaway
from project.gateaways.item_gateaway import ItemGateaway
from project.services.electronic_service import ElectronicService
from project.gateaways.inventory_gateaway import InventoryGateaway
from re import match
from uuid import uuid4
import traceback


class MonitorService():

    # Creates a monitor that is valid
    @staticmethod
    def create_monitor(brand, price, weight, dimensions):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight):
                monitor = Monitor(model=str(uuid4()), brand=brand, price=price, weight=weight, dimensions=dimensions)
                ItemGateaway.insert_into_db(monitor)
                MonitorGateaway.insert_into_db(monitor)

                logger.info('Monitor created successfully!')

                return monitor

        except Exception as e:
            logger.error(traceback.format_exc())

    # Queries the list of all monitors and their count
    @staticmethod
    def get_all_monitors():
        try:
            rows = MonitorGateaway.query_filtered_by()
            monitors = MonitorService.get_monitors_from_rows(rows)
            monitors_with_count = []

            if monitors:
                for monitor in monitors:
                    count = InventoryGateaway.get_count('monitors', monitor.model)
                    monitors_with_count.append([monitor, count])
                return monitors_with_count
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())

    # Returns all monitors from rows taken from db
    @staticmethod
    def get_monitors_from_rows(rows):
        if rows:
            monitors = []
            for row in rows:
                monitor = Monitor(row[0], row[1], row[2], row[3], row[4])
                monitors.append(monitor)
            if monitors:
                return monitors
            else:
                return None
        else:
            return None

    def delete_monitor(self):
        delete_item('monitors', self.model)