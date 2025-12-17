import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import create_app

class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_register_customer(self):
        response = self.app.post('/customers/', json={
            'name': 'Test User',
            'email': 'testuser@mail.com',
            'password': 'password123',
            'phone': '123-456-7890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_register_customer_missing_field(self):
        response = self.app.post('/customers/', json={
            'name': 'Test User',
            'email': 'testuser@mail.com',
            'password': 'password123'
        })
        self.assertNotEqual(response.status_code, 201)

    def test_get_customers(self):
        response = self.app.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('customers', response.get_json())

    def test_customer_login(self):
        # Register first
        self.app.post('/customers/', json={
            'name': 'Login User',
            'email': 'login@mail.com',
            'password': 'password123',
            'phone': '123-456-7890'
        })
        response = self.app.post('/customers/login', json={
            'email': 'login@mail.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_customer_login_invalid(self):
        response = self.app.post('/customers/login', json={
            'email': 'notfound@mail.com',
            'password': 'wrongpass'
        })
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
