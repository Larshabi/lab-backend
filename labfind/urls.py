from django.contrib import admin
from django.urls import path, include

admin.site.site_header  =  "Medical Laboratory Directory admin"  
admin.site.site_title  =  "Medical Laboratory Directory admin site"
admin.site.index_title  =  "Medical Laboratory Direrctory Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lab/', include('lab.urls'))
]

