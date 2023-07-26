from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Laboratory, Test, TestCategories
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import LaboratorySerializer, TestSerializer, LabTestSerializer, TestCategoriesSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from geopy.geocoders import GoogleV3
from django.db.models import Q
import requests
google_key= 'AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA'

class LaboratoryListView(ListAPIView):
    serializer_class = LaboratorySerializer
    queryset = Laboratory.objects.all()
    
class LaboratoryTestsView(ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        laboratory_id = self.kwargs.get('laboratory_id')
        laboratory = get_object_or_404(Laboratory, id=laboratory_id)

        # Get all Test objects associated with the given laboratory
        tests = Test.objects.filter(testprices__laboratory=laboratory).distinct()
        print(tests)

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
            Q(city__icontains=search_query)
        ).distinct()
        return queryset
    

class NearbyLaboratoryView(APIView):
    def post(self, request):
        geolocator = GoogleV3(api_key=google_key)
        coord = str(request.data['lat']) + ', '+ str(request.data['long'])
        locations = geolocator.reverse(coord)
        location_split = locations[0].split(", ")
        city = location_split[-3]
        laboratory = Laboratory.objects.filter(city=city)
        if not laboratory or laboratory is None:
            return Response({
                'message':'There are no nearby laboratories around'
            })
        laboratory_serializer = LaboratorySerializer(laboratory, many=True)
        return Response(laboratory_serializer.data)
    

class LaboratoryAndTestSearchView(APIView):
    def post(self, request):
        query = request.query_params.get('query', '')
        search_category = request.data['search_category']
        print(search_category)
        response_data = {
            'message':'Query not Found'
        }
        print(search_category == 'test_category')
        if search_category == 'test_name':
            test_results = Test.objects.filter(name__icontains=query)
            test_serializer = TestSerializer(test_results, many=True)
            response_data = {
                'test_result':test_serializer.data
            }
            return Response(response_data)
        elif search_category == 'test_category':
            category = TestCategories.objects.filter(name__icontains=query)
            new_category = TestCategories.objects.get(name=query)
            tests  = new_category.test_set.all()
            print(tests)
            response_data = {
                # 'category_result':TestCategoriesSerializer(category),
                'test_result':TestSerializer(tests, many=True).data
            }
            return Response(response_data, status.HTTP_200_OK)
        elif search_category == 'city':
            location_results = Laboratory.objects.filter(city__icontains=query)
            location_serializer = LaboratorySerializer(location_results, many=True)
            response_data = {
                'laboratories':location_serializer.data
            }
            return Response(response_data)
        
        elif search_category == 'laboratory':
            laboratory_results = Laboratory.objects.filter(name__icontains=query)
            print(laboratory_results)
            laboratory_serializer = LaboratorySerializer(laboratory_results, many=True)
            response_data = {
                'laboratories':laboratory_serializer.data
            }
            return Response(response_data)
        return Response(response_data)


    
class FindPlace(APIView):
    def get(self, request):
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=FGHQ+F7W,%20220101,%20Ife,%20Osun&inputtype=textquery&fields=geometry&key=AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA"
        response = requests.request("GET", url, headers={}, data={})
        responseData = {
            "data":response.text
        }
        return Response(responseData)