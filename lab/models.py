from django.db import models

class Laboratory(models.Model):
    class Meta:
        verbose_name = 'Laboratory'
        verbose_name_plural = 'Laboratories'
    name = models.CharField(max_length=255)
    address = models.TextField()
    google_address = models.TextField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class TestCategories(models.Model):
    class Meta:
        verbose_name = 'Test Category'
        verbose_name_plural = 'Test Categories'
        
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Test(models.Model):
    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
    name = models.CharField(max_length=255)
    category = models.ForeignKey(TestCategories, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class TestPrices(models.Model):
    class Meta:
        verbose_name = 'Test Price'
        verbose_name = 'Test Prices'
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits= 12)
    
    def __str__(self):
        return f"{self.test.name} - {self.laboratory.name}: {self.price}"
    

    