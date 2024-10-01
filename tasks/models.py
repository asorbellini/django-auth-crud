from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecomplete = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Hacer que la tarea se vea con su propio titulo
    
    def __str__(self) -> str:
        return self.title + " - " + self.user.username