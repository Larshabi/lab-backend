from django.contrib import admin
from .models import TestCategories, Test, Laboratory


admin.site.register(Test)
admin.site.register(TestCategories)
admin.site.register(Laboratory)
