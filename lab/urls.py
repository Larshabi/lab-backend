from django.urls import path
from .views import *

urlpatterns = [
    path('list-lab', LaboratoryListView.as_view(), name='laboratories'),
    path('search', LaboratoryAndTestSearchView.as_view()),
    path('laboratory/tests/<int:laboratory_id>/', LaboratoryTestsView.as_view(), name='laboratory-tests'),
    path('tests/<int:id>/', TestDetailView.as_view(), name='test-detail'),
    path('tests/search/', TestSearchView.as_view(), name='test-search'),
]
