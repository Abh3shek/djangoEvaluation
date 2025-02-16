from django.db import models
from django.conf import settings
from apps.models import AndroidApp

def screenshot_upload_path(instance, filename):
    # This function defines the upload path for screenshots
    return f"user_{instance.user.id}/screenshots/app_{instance.app.id}/{filename}"

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app = models.ForeignKey(AndroidApp, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to=screenshot_upload_path, blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task for {self.user.username} - {self.app.name}"
