from django.db import models
from django.contrib.auth.models import User

class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    processed_image = models.ImageField(upload_to='processed/', null=True, blank=True)
    result_csv = models.FileField(upload_to='reports/csv/', null=True, blank=True)
    result_xlsx = models.FileField(upload_to='reports/xlsx/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)