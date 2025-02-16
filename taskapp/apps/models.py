from django.db import models

# Create your models here.

class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=0)
    # Optionally, add a description or other fields
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
