from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Laboratory, Test, TestCategories, TestPrices
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import LaboratorySerializer, TestSerializer, LabTestSerializer, TestCategoriesSerializer, TestLabSerializer, TestPriceSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
# from geopy.geocoders import GoogleV3
from django.db.models import Q
# import requests
google_key= 'AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA'

class LaboratoryListView(ListAPIView):
    serializer_class = LaboratorySerializer
    queryset = Laboratory.objects.all()
    
class LaboratoryTestsView(ListAPIView):
    serializer_class = TestLabSerializer

    def get_queryset(self):
        laboratory_id = self.kwargs.get('laboratory_id')
        laboratory = get_object_or_404(Laboratory, id=laboratory_id)
        tests = Test.objects.filter(testprices__laboratory=laboratory).distinct()
        test_price = TestPrices.objects.filter(laboratory__id=laboratory_id)
        return tests
    
    
class TestDetailView(RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    lookup_field = 'id'




class TestSearchView(ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        search_query = query_params.get('q', '')
        queryset = Test.objects.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(testprices__laboratory__name__icontains=search_query) |
            Q(testprices__laboratory__city__icontains=search_query)
        ).distinct()
        return queryset
class CitySearchView(ListAPIView):
    serializer_class = LaboratorySerializer
    def get_queryset(self):
        query_params = self.request.query_params
        search_query = query_params.get('q', '')
        queryset = Laboratory.objects.filter(
            Q(city__icontains=search_query) |
            Q(name__icontains=search_query)
        ).distinct()
        return queryset
    


    
# class FindPlace(APIView):
#     def get(self, request):
#         url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=FGHQ+F7W,%20220101,%20Ife,%20Osun&inputtype=textquery&fields=geometry&key=AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA"
#         response = requests.request("GET", url, headers={}, data={})
#         responseData = {
#             "data":response.text
#         }
#         return Response(responseData)