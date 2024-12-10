import os
import logging
from decimal import Decimal
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, init_db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"

class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ############################################################
    # Test Cases
    ############################################################

    # Task 3a: READ Test Case
    def test_read_product(self):
        """It should Read a single Product"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["id"], test_product.id)
        self.assertEqual(data["name"], test_product.name)

    # Task 3b: UPDATE Test Case
    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = self._create_products(1)[0]
        updated_data = {"name": "Updated Name", "price": 20.00}
        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["name"], "Updated Name")
        self.assertEqual(Decimal(updated_product["price"]), 20.00)

    # Task 3c: DELETE Test Case
    def test_delete_product(self):
        """It should Delete an existing Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure it no longer exists
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Task 3d: LIST ALL Test Case
    def test_list_all_products(self):
        """It should List all Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # Task 3e: LIST BY NAME Test Case
    def test_list_by_name(self):
        """It should List Products by Name"""
        product_name = "Unique Product"
        test_product = ProductFactory(name=product_name)
        self.client.post(BASE_URL, json=test_product.serialize())
        response = self.client.get(f"{BASE_URL}?name={product_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], product_name)

    # Task 3f: LIST BY CATEGORY Test Case
    def test_list_by_category(self):
        """It should List Products by Category"""
        category = "ELECTRONICS"
        test_product = ProductFactory(category=category)
        self.client.post(BASE_URL, json=test_product.serialize())
        response = self.client.get(f"{BASE_URL}?category={category}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], category)

    # Task 3g: LIST BY AVAILABILITY Test Case
    def test_list_by_availability(self):
        """It should List Products by Availability"""
        test_product = ProductFactory(available=True)
        self.client.post(BASE_URL, json=test_product.serialize())
        response = self.client.get(f"{BASE_URL}?available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertTrue(data[0]["available"])
