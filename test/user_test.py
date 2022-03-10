# import unittest


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


# if __name__ == '__main__':
#     unittest.main()
import unittest
from app.models import User
class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(password = 'Access')
    def test_password_setter(self):
        self.assertTrue(self.new_user.password_secure is not None)
    def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_user.password
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('Access'))