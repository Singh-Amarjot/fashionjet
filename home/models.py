from django.db import models
from base.models import BaseModel 
class contact(BaseModel):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=200)
    subject=models.CharField(max_length=50)
    desc=models.TextField(max_length=300)
    def __str__(self):
        return self.name
# Create your models here.
