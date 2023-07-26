from rest_framework import serializers
from .models import Laboratory, TestCategories, Test, TestPrices
# from geopy.geocoders import GoogleV3 
# import requests

reverse = '461033145172484425100x127157'
google_key= 'AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA'

class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = '__all__'

class TestCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategories
        fields = '__all__'
        
class TestPriceSerializer(serializers.ModelSerializer):
    laboratory = LaboratorySerializer()

    class Meta:
        model = TestPrices
        fields = ('laboratory', 'price')

class TestSerializer(serializers.ModelSerializer):
    category = TestCategoriesSerializer()
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            'id',
            'category',
            'name',
            'prices'
        ]
    def get_prices(self, obj):
        prices = TestPrices.objects.filter(test=obj)
        serializer = TestPriceSerializer(prices, many=True)
        return serializer.data
        

class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields =['latitude', 'longitude']
    
    def create(self, validate_data):
        geolocator = GoogleV3(api_key=google_key)
        locations = geolocator.reverse("7.5053399, 4.50437")
        location_split = locations[0].split(", ")
        city = location_split[-3]
        laboratory = Laboratory.objects.filter(city=city)
        return laboratory
    
class LabTestSerializer(serializers.ModelSerializer):
    category = TestCategoriesSerializer(read_only=True)
    class Meta:
        model = Test
        fields = [
            'id',
            'name',
            'price',
            'category'
        ]

