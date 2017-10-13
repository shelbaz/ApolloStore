
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.television_model import Television
from project.gateways import delete_item
from project.gateways.television_gateway import TelevisionGateway
from project.gateways.item_gateway import ItemGateway
from project.services.electronic_service import ElectronicService
from project.services.inventory_service import InventoryService
from project.gateways.inventory_gateway import InventoryGateway
from project.identityMap import IdentityMap
from re import match
from uuid import uuid4
import traceback


class TelevisionService():

    identityMap = IdentityMap()

    # Creates a television that is valid
    @staticmethod
    def create_television(brand, price, weight, type, dimensions):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight):
                television = Television(model=str(uuid4()), brand=brand, price=price, weight=weight, type=type, dimensions=dimensions)
                ItemGateway.insert_into_db(television)
                TelevisionGateway.insert_into_db(television)
                TelevisionService.identityMap.set(television.model, television)

                logger.info('Television created successfully!')

                return television

        except Exception as e:
            logger.error(traceback.format_exc())

    # Queries the list of all televisions and their count
    @staticmethod
    def get_all_televisions():
        try:
            rows = TelevisionGateway.query_filtered_by()
            televisions = TelevisionService.get_televisions_from_rows(rows)
            televisions_with_count = []

            if televisions:
                for television in televisions:
                    count = InventoryGateway.get_count('televisions', television.model)
                    televisions_with_count.append([television, count])
                return televisions_with_count
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())

    # Returns all televisions from rows taken from db
    @staticmethod
    def get_televisions_from_rows(rows):
        if rows:
            televisions = []
            for row in rows:
                #check identity map
                if TelevisionService.identityMap.hasId(row[0]):
                    television = TelevisionService.identityMap.getObject(row[0])
                else:
                    television = Television(row[0], row[1], row[2], row[3], row[4], row[5])
                    TelevisionService.identityMap.set(television.model, television)        

                televisions.append(television)
            
            if televisions:
                return televisions
            else:
                return None
        else:
            return None
