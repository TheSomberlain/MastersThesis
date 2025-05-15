from django.db import models
from django.contrib.auth.models import User

class ProcessedImage(models.Model):
    image_file = models.ImageField(upload_to='results/', null = True)
    original_file = models.ImageField(null = True)
    is_created_by_auth_user = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DetectedROI(models.Model):
    parent_image = models.ForeignKey(ProcessedImage, on_delete=models.CASCADE, related_name='rois')
    roi_file = models.ImageField(upload_to='results/rois/')
    label = models.CharField(max_length=255, blank=True, null=True)
    x_min = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_max = models.FloatField(null=True)

class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(ProcessedImage, related_name='reports')
    name = models.CharField(max_length=255, blank=True, null=True)
    result_csv = models.FileField(upload_to='reports/csv/', null=True, blank=True)
    result_xlsx = models.FileField(upload_to='reports/xlsx/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)