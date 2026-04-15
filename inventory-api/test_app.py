import unittest
from app import app, inventory

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        # Reset the inventory before each test
        global inventory
        inventory.clear()

    #  CREATE
    def test_create_item(self):
        response = self.client.post('/items', json={
            "name": "Bread",
            "quantity": 5
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "Bread")

    # READ ALL
    def test_get_items(self):
        # Add item first
        self.client.post('/items', json={
            "name": "Milk",
            "quantity": 3
        })

        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)

    #  UPDATE 
    def test_update_item(self):
        # Create item first
        create_res = self.client.post('/items', json={
            "name": "Eggs",
            "quantity": 10
        })

        item = create_res.get_json()
        item_id = item["id"]

        # Update item
        response = self.client.patch(f'/items/{item_id}', json={
            "quantity": 20
        })

        self.assertEqual(response.status_code, 200)
        updated = response.get_json()
        self.assertEqual(updated["quantity"], 20)

    #  DELETE
    def test_delete_item(self):
        # Create item first
        create_res = self.client.post('/items', json={
            "name": "Juice",
            "quantity": 2
        })

        item = create_res.get_json()
        item_id = item["id"]

        # Delete item
        response = self.client.delete(f'/items/{item_id}')
        self.assertEqual(response.status_code, 200)

    
    def test_update_nonexistent_item(self):
        response = self.client.patch('/items/999', json={
            "quantity": 50
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()