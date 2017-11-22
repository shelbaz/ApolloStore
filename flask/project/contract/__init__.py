from flask import g
from project.orm import Mapper
class Contract(object):

    def purchase_item(func):
        def new_func(model):
            # Checks pre-condition
            assert not g.user.admin
            func(model)
        return new_func

    def return_item_to_store(func):
        def new_func(model):
            from project.controllers.purchase import PurchaseController
            # Checks pre-condition
            rows = Mapper.query('purchases', model_id=model, user_id=g.user.id)
            inventory_items = PurchaseController.get_purchases_from_rows(rows)
            assert inventory_items[0]

            rows = Mapper.query('purchases', user_id=g.user.id)
            inventory_items = PurchaseController.get_purchases_from_rows(rows)
            size = len(inventory_items)
            func(model)
            # Checks post-condition
            rows = Mapper.query('purchases', user_id=g.user.id)
            inventory_items = PurchaseController.get_purchases_from_rows(rows)
            assert len(inventory_items) == size - 1
        return new_func

    def add_to_cart(func):
        def new_func(model):
            from project.controllers.inventory import InventoryController
            from project.controllers.cart import CartController
            # Checks pre-condition
            rows = Mapper.query('inventories', model=model)
            inventory_item = InventoryController.get_inventory_items_from_rows(rows)[0]
            assert inventory_item.locked == False

            rows = Mapper.query('carts', user_id=g.user.id)
            carts = CartController.get_cart_items_from_rows(rows)
            size = len(carts)
            func(model)
            # Checks post-condition
            rows = Mapper.query('inventories', model=model)
            inventory_item = InventoryController.get_inventory_items_from_rows(rows)[0]
            assert inventory_item.locked == True

            rows = Mapper.query('carts', user_id=g.user.id, inventory_id=inventory_item.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert carts

            rows = Mapper.query('carts', user_id=g.user.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert len(carts) == size + 1
        return new_func

    def remove_from_cart(func):
        def new_func(model):
            from project.controllers.inventory import InventoryController
            from project.controllers.cart import CartController
            # Checks pre-condition
            rows = Mapper.query('inventories', model=model)
            inventory_item = InventoryController.get_inventory_items_from_rows(rows)[0]
            assert inventory_item.locked == True

            rows = Mapper.query('carts', user_id=g.user.id, inventory_id=inventory_item.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert carts

            rows = Mapper.query('carts', user_id=g.user.id)
            carts = CartController.get_cart_items_from_rows(rows)
            size = len(carts)
            func(model)
            # Checks post-condition
            rows = Mapper.query('carts', user_id=g.user.id, inventory_id=inventory_item.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert not carts

            rows = Mapper.query('inventories', model=model)
            inventory_item = InventoryController.get_inventory_items_from_rows(rows)[0]
            assert inventory_item.locked == False

            rows = Mapper.query('carts', user_id=g.user.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert len(carts) == size - 1
        return new_func

    def checkout(func):
        def new_func():
            from project.controllers.cart import CartController
            # Checks pre-condition
            rows = Mapper.query('carts', user_id=g.user.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert len(carts) > 0
            func()
            # Checks post-condition
            rows = Mapper.query('carts', user_id=g.user.id)
            carts = CartController.get_cart_items_from_rows(rows)
            assert len(carts) == 0
        return new_func
