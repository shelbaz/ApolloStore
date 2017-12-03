# ------------------------------------------------------
# This is the entry point of the Flask application.
# ------------------------------------------------------


from project import create_app, logger
from flask_script import Manager
import coverage
import unittest
from project.gateways.database_setup import create_tables, drop_tables


# The logger should always be used instead of a print(). You need to import it from
# the project package. If you want to understand how to use it properly and why you
# should use it, check: http://bit.ly/2nqkupO
logger.info('Server has started.')


# Defines which parts of the code to includ and omit when calculating code coverage.
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'tests/*',
        'project/website/*'
    ]
)
COV.start()


# Creates the Flask application object that we use to initialize things in the app.
app = create_app()


# Initializes the Manager object, which allows us to run terminal commands on the
# Flask application while it's running.
manager = Manager(app)


# Creates all the tables from the models package
with app.app_context():
    create_tables()


# While the application is running, you can run the following command in a new terminal:
# 'docker-compose run --rm flask python manage.py cov' to run all the tests in the
# 'tests' directory. If all the tests pass, it will generate a coverage report.
@manager.command
def cov():
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    else:
        return 1


# Enter 'docker-compose run --rm flask python manage.py test' to run all the
# tests in the 'tests' directory, but provides no coverage report.
@manager.command
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


# Enter 'docker-compose run --rm flask python manage.py test_one NAME_OF_FILE' to run only one
# test file in the 'tests' directory. It provides no coverage report.
#
# Example: 'docker-compose run --rm flask python manage.py test_one test_website'
# Note that you do not need to put the extension of the test file.
@manager.command
def test_one(test_file):
    tests = unittest.TestLoader().discover('tests', pattern=test_file + '.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def create():
    create_tables()

@manager.command
def drop():
    import traceback
    try:
        drop_tables()
    except Exception:
        logger.error(traceback.format_exc())

# For use to resetup application with users and data after an update
@manager.command
def init_store():
    import traceback
    try:
        drop()
        create()
        create_users()
        create_items()
    except Exception:
        logger.error(traceback.format_exc())

# For use to create test users
@manager.command
def create_users():
    import traceback
    try:
        from project.controllers.authentication import AuthenticationController
        AuthenticationController.create_user('Admin', 'One', '4378473 north', 'admin1@test.com', 'test', '3736363663', 'True')
        AuthenticationController.create_user('Admin', 'Two', '437843 north', 'admin2@test.com', 'test', '337737373', 'True')
        AuthenticationController.create_user('Client', 'One', '4378473 north', 'client1@test.com', 'test', '3736363663', 'False')
        AuthenticationController.create_user('Client', 'Two', '437843 north', 'client2@test.com', 'test', '337737373', 'False')
        AuthenticationController.create_user('Client', 'Three', '437843 north', 'client3@test.com', 'test', '337737373', 'False')
        AuthenticationController.create_user('Shawn', 'Elbaz', '4847 north', 'shawn@shawn.com', 'lool', '4747747474', 'False')
        AuthenticationController.create_user('Shawn', 'Elbaz', '4847 north', 'shawn@test.com', 'lool', '4747747474', 'True')
    except Exception:
        logger.error(traceback.format_exc())


@manager.command
def test_aspect():
    import traceback
    try:
        from project.controllers.monitor import MonitorController
        monitor = MonitorController.create_monitor('Asus', 300, 5, '25x30')
        from project import identity_map
        identity_map.delete(monitor.model)
        identity_map.getObject(monitor.model)
    except Exception:
        logger.error(traceback.format_exc())

# For use to create test items and add to inventory 
@manager.command
def create_items():
    import traceback
    try:
        from project.controllers.desktop import DesktopController
        from project.controllers.laptop import LaptopController
        from project.controllers.monitor import MonitorController
        from project.controllers.tablet import TabletController
        from project.controllers.inventory import InventoryController

        invModels = []

        invModels.append(LaptopController.create_laptop('Asus', 990, 3, '10x15', 'AMD', 256, 2, 1080, 'good', 'Windows 10', True, True))
        invModels.append(LaptopController.create_laptop('Lenovo', 550, 3, '10x10', 'intel', 256, 4, 1080, 'good', 'Windows 8', False, True))
        invModels.append(LaptopController.create_laptop('Dell', 500, 2, '15x10', 'AMD', 256, 6, 1080, 'good', 'Windows 10', False, True))
        invModels.append(LaptopController.create_laptop('Acer', 668, 3, '10x12', 'ARM', 128, 8, 1080, 'good', 'Windows 7', True, True))
        invModels.append(LaptopController.create_laptop('Toshiba', 920, 3, '10x10', 'intel', 512, 2, 1080, 'good', 'Windows 10', False, True))
        invModels.append(LaptopController.create_laptop('HP', 880, 3, '12x10', 'intel', 1000, 6, 1080, 'good', 'Windows 7', False, True))
        invModels.append(LaptopController.create_laptop('Asus', 550, 2, '10x10', 'intel', 256, 4, 1080, 'good', 'Windows 8', False, True))
        invModels.append(LaptopController.create_laptop('Lenovo', 890, 3, '10x13', 'ARM', 1000, 6, 1080, 'good', 'Windows 7', False, True))


        invModels.append(TabletController.create_tablet('Asus', 100, 10, '10x15', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice'))
        invModels.append(TabletController.create_tablet('Dell', 150, 10, '15x10', '90x90', 'ARM', 256, 1, 1080, 'good', 'Windows 10', 'nice'))
        invModels.append(TabletController.create_tablet('Samsung', 200, 10, '10x12', '80x90', 'intel', 256, 2, 1080, 'good', 'Windows 8', 'nice'))
        invModels.append(TabletController.create_tablet('Apple', 299, 10, '12x10', '100x100', 'ARM', 512, 4, 1080, 'good', 'iOS', 'nice'))
        invModels.append(TabletController.create_tablet('Canon', 305, 10, '10x11', '90x90', 'intel', 256, 2, 1080, 'good', 'Windows 8', 'nice'))
        invModels.append(TabletController.create_tablet('Lenovo', 355, 10, '11x10', '80x90', 'AMD', 128, 4, 1080, 'good', 'Windows 10', 'nice'))
        invModels.append(TabletController.create_tablet('Apple', 350, 10, '14x12', '90x90', 'intel', 512, 1, 1080, 'good', 'iOS', 'nice'))
        invModels.append(TabletController.create_tablet('Dell', 100, 10, '10x15', '100x100', 'AMD', 256, 2, 1080, 'good', 'Windows 10', 'nice'))


        invModels.append(MonitorController.create_monitor('Asus', 669, 10, '125x100'))
        invModels.append(MonitorController.create_monitor('Dell', 600, 10, '150x100'))
        invModels.append(MonitorController.create_monitor('HP', 550, 10, '170x100'))
        invModels.append(MonitorController.create_monitor('Acer', 700, 11, '125x100'))
        invModels.append(MonitorController.create_monitor('Dell', 870, 12, '150x100'))
        invModels.append(MonitorController.create_monitor('HP', 999, 13, '170x100'))

        invModels.append(DesktopController.create_desktop('Asus', 600, 10, 'ARM', 256, 2, 1080, '100x100'))
        invModels.append(DesktopController.create_desktop('Dell', 550, 10, 'ARM', 256, 1, 1080, '90x100'))
        invModels.append(DesktopController.create_desktop('Lenovo', 590, 10, 'intel', 256, 2, 1080, '90x100'))
        invModels.append(DesktopController.create_desktop('HP', 666, 10, 'ARM', 256, 2, 1080, '100x90'))
        invModels.append(DesktopController.create_desktop('Toshiba', 780, 10, 'intel', 256, 1, 1080, '110x100'))
        invModels.append(DesktopController.create_desktop('Microsoft', 790, 10, 'AMD', 256, 2, 1080, '100x110'))
        invModels.append(DesktopController.create_desktop('Asus', 550, 10, 'intel', 256, 4, 1080, '89x90'))
        invModels.append(DesktopController.create_desktop('Dell', 780, 10, 'intel', 256, 1, 1080, '109x100'))
        invModels.append(DesktopController.create_desktop('Lenovo', 800, 10, 'AMD', 256, 4, 1080, '100x110'))

        for item in invModels: 
            InventoryController.add_item_to_inventory(item.model, item.__class__.__name__)
    except Exception:
        logger.error(traceback.format_exc())


# Starts the Flask app.
if __name__ == '__main__':
    manager.run()