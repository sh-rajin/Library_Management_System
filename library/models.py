from django.db import models
from accounts.models import UserLibraryAccount
from books.models import Book
# Create your models here.
    
  
class Report(models.Model):
    user = models.ForeignKey(UserLibraryAccount, related_name='report', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='report', on_delete=models.CASCADE)
    # borrow_date = models.DateField()
    # return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.book} - {self.user}"
    
    
    
class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.book}"

    
    
       
 
 
 