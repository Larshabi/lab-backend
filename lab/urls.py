from django.urls import path
from .views import *

urlpatterns = [
    path('list-lab', LaboratoryListView.as_view(), name='laboratories'),
    path('test', NearbyLaboratoryView.as_view()),
    path('search', LaboratoryAndTestSearchView.as_view()),
    path('lab-test/<str:laboratory_id>', LaboratoryTestsView.as_view()),
    path('findPlace', FindPlace.as_view())
]
