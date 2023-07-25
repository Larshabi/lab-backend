from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Laboratory, Test, TestCategories
from rest_framework import status
from .serializer import LaboratorySerializer, TestSerializer, LabTestSerializer, TestCategoriesSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView
from geopy.geocoders import GoogleV3
import requests
google_key= 'AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA'

class LaboratoryListView(ListAPIView):
    serializer_class = LaboratorySerializer
    queryset = Laboratory.objects.all()
    

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



class LaboratoryTestsView(APIView):
    def get(self, request, laboratory_id):
        try:
            laboratory = Laboratory.objects.get(id=laboratory_id)
        except Laboratory.DoesNotExist:
            return Response({'error': 'Laboratory not found'}, status=404)

        tests_performed = laboratory.test_set.all()
        test_serializer = LabTestSerializer(tests_performed, many=True)

        return Response(test_serializer.data)
    
    
class FindPlace(APIView):
    def get(self, request):
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=FGHQ+F7W,%20220101,%20Ife,%20Osun&inputtype=textquery&fields=geometry&key=AIzaSyDA-wB9OtVQ3DhdSmPz8kwp5gdM0ZwZFxA"
        response = requests.request("GET", url, headers={}, data={})
        responseData = {
            "data":response.text
        }
        return Response(responseData)