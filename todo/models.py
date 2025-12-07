from django.db import models

# Create your models here.

class Task(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank= True)
    comlated = models.BooleanField(default= False)
    status = models.CharField(max_length=50, default='pending')
    priority = models.IntegerField(default=1)
    category = models.CharField(max_length=150, blank= True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.CharField(max_length=150, blank= True)
    assigned_to = models.CharField(max_length=150, blank= True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
