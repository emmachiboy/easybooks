from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.TextField()
    summary = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="books/", null=True, blank=True)
    pdf = models.FileField(upload_to="pdfs/", null= True, blank=True)
    html = models.FileField(upload_to="htmls/", null=True, blank= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"