import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import create_app

class TestAssignments(unittest.TestCase):
    def setUp(self):
        import random
        self.app = create_app().test_client()
        self.rand = str(random.randint(10000, 99999))
        self.customer_email = f'assign{self.rand}@mail.com'
        self.customer_phone = f'123-456-{self.rand[-4:]}'
        self.mechanic_email = f'joe{self.rand}@mail.com'
        self.mechanic_phone = f'321-654-{self.rand[-4:]}'
        # Register a customer
        customer_resp = self.app.post('/customers/', json={
            'name': 'Assign User',
            'email': self.customer_email,
            'password': 'password123',
            'phone': self.customer_phone
        })
        self.customer_id = customer_resp.get_json().get('id') if customer_resp.is_json else 1
        # Create a service ticket
        ticket_resp = self.app.post('/service-tickets/', json={
            'VIN': f'1HGCM82633A{self.rand}',
            'description': 'Brake check',
            'make': 'Toyota',
            'model': 'Camry',
            'service_date': '2025-12-15',
            'year': 2021,
            'customer_id': self.customer_id
        })
        self.ticket_id = ticket_resp.get_json().get('id') if ticket_resp.is_json else 1

    def test_assign_mechanic(self):
        # Register a mechanic
        mech_resp = self.app.post('/mechanics/', json={
            'name': 'Mechanic Joe',
            'email': self.mechanic_email,
            'phone': self.mechanic_phone,
            'salary': 50000.0
        })
        print('Mechanic creation response:', mech_resp.status_code, mech_resp.data)
        mechanic_id = mech_resp.get_json().get('id') if mech_resp.is_json else 1
        response = self.app.post('/service-tickets/mechanic-service-ticket/', json={
            'mechanic_id': mechanic_id,
            'service_ticket_id': self.ticket_id,
            'status': 'assigned'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.get_json())

    def test_assign_mechanic_missing_field(self):
        response = self.app.post('/service-tickets/mechanic-service-ticket/', json={
            'mechanic_id': 99999,
            'service_ticket_id': 99999
        })
        self.assertNotEqual(response.status_code, 201)

    def test_get_assignments(self):
        response = self.app.get('/service-tickets/mechanic-service-ticket/')
        print('Get assignments response:', response.status_code, response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

if __name__ == '__main__':
    unittest.main()

