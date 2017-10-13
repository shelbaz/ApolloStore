
from project import logger
from project.models.tablet_model import Tablet
from project.services.electronic_service import ElectronicService
from project.identityMap import IdentityMap
from project.gateways import get_inventory_count
from uuid import uuid4
import traceback


class TabletService():

    identityMap = IdentityMap()

    # Creates a tablet that is valid
    def create_tablet(brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight) and ElectronicService.validate_ram_size(ram_size) and ElectronicService.validate_cpu_cores(cpu_cores) and ElectronicService.validate_hd_size(hd_size):
                tablet = Tablet(model=str(uuid4()), brand=brand, price=price, weight=weight, display_size=display_size, dimensions=dimensions, processor=processor,
                                ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, battery=battery, os=os, camera_info=camera_info)
                tablet.insert()
                TabletService.identityMap.set(tablet.model, tablet)

                logger.info('Tablet created successfully!')

                return tablet

        except Exception:
            logger.error(traceback.format_exc())

    # Queries the list of all tablets and their count
    @staticmethod
    def get_all_tablets():
        try:
            rows = Tablet.query()
            tablets = TabletService.get_tablets_from_rows(rows)
            tablets_with_count = []

            if tablets:
                for tablet in tablets:
                    count = get_inventory_count('tablets', tablet.model)
                    tablets_with_count.append([tablet, count])
                return tablets_with_count
            else:
                return None
        except Exception:
            logger.error(traceback.format_exc())

    # Returns all tablets from rows taken from db
    @staticmethod
    def get_tablets_from_rows(rows):
        tablets = []

        if rows:
            for row in rows:
                #check identity map
                if TabletService.identityMap.hasId(row[0]):
                    tablet = TabletService.identityMap.getObject(row[0])
                else:
                    tablet = Tablet(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                row[11], row[12])
                    TabletService.identityMap.set(tablet.model, tablet)

                tablets.append(tablet)
            
            if tablets:
                return tablets
            else:
                return None
        else:
            return None
