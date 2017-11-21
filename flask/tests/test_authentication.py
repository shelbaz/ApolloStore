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
from tests.base_authentication import BaseTestCase
from project.controllers.authentication import  AuthenticationController
from project.orm import Mapper


# This class inherits from the base class in 'base_authentication.py', in order to
# get the create_app, setUp and tearDown methods.
class TestAuthentication(BaseTestCase):
    def test_validate_email(self):
        with self.client:
            self.assertTrue(AuthenticationController.validate_email('soen343@gmail.com'))
            self.assertFalse(AuthenticationController.validate_email(''))
            self.assertFalse(AuthenticationController.validate_email('soen343@'))
            self.assertFalse(AuthenticationController.validate_email('soen343@@'))

    def test_validate_name(self):
        with self.client:
            self.assertFalse(AuthenticationController.validate_name(''))
            self.assertFalse(
                AuthenticationController.validate_name('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'))
            self.assertFalse(AuthenticationController.validate_name('23232'))
            self.assertFalse(AuthenticationController.validate_name('muku1234'))
            self.assertTrue(AuthenticationController.validate_name('corey'))
            self.assertTrue(AuthenticationController.validate_name('COREY'))
            self.assertTrue(AuthenticationController.validate_name('Murey'))

    def test_validate_password(self):
        with self.client:
            self.assertFalse(AuthenticationController.validate_password('abcd12'))
            self.assertFalse(AuthenticationController.validate_password('1234567890123456789011'))
            self.assertFalse(AuthenticationController.validate_password('Abc 12'))
            self.assertTrue(AuthenticationController.validate_password('Murey2017'))

    def test_validate_create_user(self):
        with self.client:
            user = AuthenticationController.create_user('Test', 'Tester', '123 Test', 'testing@gmail.com', 'testing111', '5141234567', False)

            self.assertEqual('Test', user.first_name)
            self.assertEqual('Tester', user.last_name)
            self.assertEqual('testing@gmail.com', user.email)
            self.assertEqual('5141234567', user.phone)
            self.assertFalse(user.admin)

    def test_register_user_endpoint(self):
        with self.client:
            request_data = dict(password='testpasswO1!rd',
                                email='test@example.com',
                                firstName='radu',
                                lastName='raicea',
                                address='123213432g',
                                phone='34543534',
                                admin=True)
            self.client.post('/register', data=request_data, content_type='application/x-www-form-urlencoded')

            rows = Mapper.query('users', email=request_data['email'])
            user= AuthenticationController.get_user_from_rows(rows)

            self.assertTrue(user)

    def test_delete_account(self):
        with self.client:
            request_data = dict(password='test',
                                email='test@test.com',
                                firstName='muku',
                                lastName='dey',
                                address='123213432g',
                                phone='34543534',
                                admin=False)

            self.client.post('/register', data=request_data, content_type='application/x-www-form-urlencoded')

            rows = Mapper.query('users', email=request_data['email'])
            user = AuthenticationController.get_user_from_rows(rows)
            self.assertNotEqual(user, None)
            result = AuthenticationController.delete_user(user.id)
            rows = Mapper.query('users', email=request_data['email'])
            deleted_user = AuthenticationController.get_user_from_rows(rows)
            self.assertEqual(deleted_user, None)

            rows = Mapper.query('purchases', user_id = user.id)
            self.assertEqual(rows, [])

            cart_rows = Mapper.query('carts', user_id = user.id)
            self.assertEqual(cart_rows, [])

# Runs the tests.
if __name__ == '__main__':
    unittest.main()
