
from project.identityMap import IdentityMap
from project.models.item import Item


class ElectronicController():

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

    @staticmethod
    def get_items_from_rows(rows):
        if rows:
            items = []
            for row in rows:
                item = Item(row[0])
                items.append(item)

            if items:
                return items
            else:
                return None

