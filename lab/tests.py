from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Test, TestCategories, Laboratory, TestPrices
from .serializer import LaboratorySerializer, TestPriceSerializer, TestSerializer
import json
from unittest import mock

class CitySearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Laboratory.objects.create(name='Precious Medical Diagnostic Center', city='Ife', google_address='FGHQ+F7W, 220101, Ife, Osun',address='FGHQ+F7W, 220101, Ife, Osun', latitude=7.485382558212946, longitude=3.53813534321048, phone='0803 408 1478', state='Osun')
        Laboratory.objects.create(name='Lab 2', city='Los Angeles')
        Laboratory.objects.create(name='Lab 3', city='Chicago')

    def test_city_search(self):
        response = self.client.get('/lab/search/', {'q': 'New'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_city_search_no_results(self):
        response = self.client.get('/lab/search/', {'q': 'Miami'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = []
        self.assertEqual(response.data, expected_data)


class TestSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data for test categories
        category1 = TestCategories.objects.create(name='Category 1')
        category2 = TestCategories.objects.create(name='Category 2')

        # Create test data for tests
        test1 = Test.objects.create(name='Test 1', category=category1)
        test2 = Test.objects.create(name='Test 2', category=category2)
        test3 = Test.objects.create(name='Test 3', category=category1)

        # Create test data for test prices
        lab1 = Laboratory.objects.create(name='Lab 1', city='New York')
        lab2 = Laboratory.objects.create(name='Lab 2', city='Los Angeles')
        TestPrices.objects.create(test=test1, laboratory=lab1, price=100)
        TestPrices.objects.create(test=test2, laboratory=lab2, price=150)
        TestPrices.objects.create(test=test3, laboratory=lab1, price=120)

    def test_test_search(self):
        response = self.client.get('/lab/tests/search/', {'q': 'Miami'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_test_search_no_results(self):
        response = self.client.get('/lab/tests/search/', {'q': 'Miami'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_data = json.loads(response.content)
        self.assertEqual(actual_data, [])
        
        

class TestDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data for test categories
        category1 = TestCategories.objects.create(name='Category 1')
        category2 = TestCategories.objects.create(name='Category 2')

        # Create test data for tests
        test1 = Test.objects.create(name='Test 1', category=category1)
        test2 = Test.objects.create(name='Test 2', category=category2)
        test3 = Test.objects.create(name='Test 3', category=category1)

        # Create test data for test prices
        lab1 = Laboratory.objects.create(name='Lab 1', city='New York')
        lab2 = Laboratory.objects.create(name='Lab 2', city='Los Angeles')
        TestPrices.objects.create(test=test1, laboratory=lab1, price=100)
        TestPrices.objects.create(test=test2, laboratory=lab2, price=150)
        TestPrices.objects.create(test=test3, laboratory=lab1, price=120)

    def test_test_detail_view(self):
        test_id = Test.objects.first().id
        response = self.client.get(f'/lab/tests/{test_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

