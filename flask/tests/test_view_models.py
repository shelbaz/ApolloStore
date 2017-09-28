# -------------------------------------------------------------------------------
# Every test file should come in pairs: a base file and the file containing
# the tests. An exception to that is the 'test_configs.py' because it is
# very simple.
#
# This is the file that contains the tests.
#
# You can call this test group file to run by running the application and
# running 'docker-compose run --rm flask python manage.py test_one test_website'
# in a separate terminal window.
# -------------------------------------------------------------------------------


import unittest
from tests.base_viewmodels import BaseTestCase
from project.services.electronics import create_laptop, create_desktop, create_monitor, create_television, create_tablet
from project.models.desktop_model import Desktop
from project.models.laptop_model import Laptop
from project.models.monitor_model import Monitor
from project.models.tablet_model import Tablet
from project.models.television_model import Television


# This class inherits from the base class in 'base_viewmodels.py', in order to
# get the create_app, setUp and tearDown methods.
class TestViewModels(BaseTestCase):
    # Test to see if the query_filtered_by function works for the Laptop class
    def test_should_return_query_results_for_laptop(self):
        with self.client:
            create_laptop('Asus', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', True, True)
            create_laptop('Lenovo', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)
            create_laptop('Dell', 500, 10, '10x10', 'intel', 256, 2, 1080, 'good', 'Windows 10', False, True)

            result1 = Laptop.query_filtered_by(brand='Asus')
            result2 = Laptop.query_filtered_by(brand='Acer')
            self.assertEqual(result1[0].brand, 'Asus')
            self.assertEqual(result2, None)

    # Test to see if the query_filtered_by function works for the Tablet class
    def test_should_return_query_results_for_tablet(self):
        with self.client:
            create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            create_tablet('Dell', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')
            create_tablet('Asus', 500, 10, '10x10', '100x100', 'intel', 256, 2, 1080, 'good', 'Windows 10', 'nice')

            result1 = Tablet.query_filtered_by(brand='Asus')
            result2 = Tablet.query_filtered_by(brand='Apple')
            self.assertEqual(len(result1), 2)
            self.assertEqual(result2, None)

    # Test to see if the query_filtered_by function works for the Desktop class
    def test_should_return_query_results_for_desktop(self):
        with self.client:
            create_desktop('Asus', 600, 10, 'intel', 256, 2, 1080, '100x100')
            create_desktop('Dell', 500, 10, 'intel', 256, 2, 1080, '100x100')
            create_desktop('Lenovo', 500, 10, 'intel', 256, 2, 1080, '100x100')

            result1 = Desktop.query_filtered_by(brand='Asus')
            result2 = Desktop.query_filtered_by(brand='Acer')
            self.assertEqual(result1[0].price, 600)
            self.assertEqual(result2, None)

    # Test to see if the query_filtered_by function works for the Monitor class
    def test_should_return_query_results_for_monitor(self):
        with self.client:
            create_monitor('Asus', 600, 10, '125x100')
            create_monitor('Dell', 600, 10, '150x100')
            create_monitor('Asus', 600, 10, '170x100')

            result1 = Monitor.query_filtered_by(dimensions='150x100')
            result2 = Monitor.query_filtered_by(brand='Acer')
            self.assertEqual(result1[0].brand, 'Dell')
            self.assertEqual(result2, None)

    # Test to see if the query_filtered_by function works for the Television class
    def test_should_return_query_results_for_television(self):
        with self.client:
            create_television('Asus', 600, 10, 'HD', '125x100')
            create_television('Asus', 600, 10, 'LED', '125x100')
            create_television('Samsung', 600, 10, '3D', '125x100')
            create_television('Asus', 600, 10, 'Smart', '125x100')

            result1 = Television.query_filtered_by(type='3D')
            result2 = Television.query_filtered_by(brand='Toshiba')
            self.assertEqual(result1[0].brand, 'Samsung')
            self.assertEqual(result2, None)


# Runs the tests.
if __name__ == '__main__':
    unittest.main()
