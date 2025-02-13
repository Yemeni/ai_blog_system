from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  
    name = models.CharField(max_length=50)  
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.name} ({self.code})"
