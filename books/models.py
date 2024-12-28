from django.db import models
from categories.models import Category

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to ='uploads/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book_category', null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.title} - {self.category.name}'