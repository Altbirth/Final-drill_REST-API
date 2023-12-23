import unittest
import warnings
from api import app
import json

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_get_addresses(self):
        response = self.app.get("/addresses")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Istres" in response.data.decode())

    def test_get_addresses_by_id(self):
        response = self.app.get("/addresses/20")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sanjiang" in response.data.decode())

    def test_post_address(self):
        response = self.app.post( "/addresses",
        json={
            "Line_1": "123 Main St",
            "Line_2": "Apt 4",
            "City": "Exampleville",
            "Zip_Postcode": "12345",
            "State_Country_Region": "Example State",
            "Country": "Example Country",
            "other_Details": "Additional details",
        },
    )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertEqual(data["message"], "addresses added successfully")
        self.assertEqual(data["rows_affected"], 1)

    def test_update_address(self):
        response = self.app.put("/addresses/61",
        json={
            "Line_1": "Updated Main St",
            "Line_2": "Apt 10",
            "City": "Updatedville",
            "Zip_Postcode": "54321",
            "State_Country_Region": "Updated State",
            "Country": "Updated Country",
            "other_Details": "Updated details",
        },
    )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["message"], "addresses updated successfully")
        self.assertEqual(data["rows_affected"], 0)

    def test_delete_address(self):
        address_id_to_delete = 65  

        response = self.app.delete(f"/addresses/{address_id_to_delete}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("addresses deleted successfully" in response.data.decode())


if __name__ == "__main__":
    unittest.main()
