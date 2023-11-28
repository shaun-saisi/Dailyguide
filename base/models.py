from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200,)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False) # Corrected the field name
    created = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 
    class Meta:  
        db_table = "tblevents"