import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import create_app

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        # Register a customer for ticket creation
        self.app.post('/customers/', json={
            'name': 'Ticket User',
            'email': 'ticket@mail.com',
            'password': 'password123',
            'phone': '123-456-7890'
        })

    def test_create_service_ticket(self):
        response = self.app.post('/service-tickets/', json={
            'VIN': '1HGCM82633A004352',
            'description': 'Oil change',
            'make': 'Honda',
            'model': 'Accord',
            'service_date': '2025-12-15',
            'year': 2020,
            'customer_id': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_create_service_ticket_missing_field(self):
        response = self.app.post('/service-tickets/', json={
            'VIN': '1HGCM82633A004352',
            'description': 'Oil change',
            'make': 'Honda',
            'model': 'Accord',
            'service_date': '2025-12-15',
            'year': 2020
        })
        self.assertNotEqual(response.status_code, 201)

    def test_get_service_tickets(self):
        response = self.app.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('service_tickets', response.get_json())

if __name__ == '__main__':
    unittest.main()
