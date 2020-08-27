from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import uuid

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    locations = models.TextField(default='')
    sample_type = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)
    pcreated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Batch(models.Model):
    STATUS_ITEM = (
        ('0', 'Uploaded'),
        ('1', 'Processing'),
        ('2', 'Completed')
    )
    name = models.CharField(max_length = 255,unique = True)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length = 255)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)
    total_images = models.IntegerField(default=0)
    failed_images = models.IntegerField(default=0)
    batch_status = models.CharField(default='0', choices = STATUS_ITEM, max_length=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.project)+"_"+str(self.name)

class ImageBank(models.Model):
    STATUS_ITEM = (
        ('0', 'Waiting'),
        ('1', 'Ready'),
        ('2', 'Failed')
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, default="", blank=True, null=True)
    URL = models.CharField(max_length=255, default="", blank=True, null=True)
    no_of_samples = models.IntegerField(default=0)
    sample_details = models.TextField(default={}, blank=True, null=True)
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(default='0', choices = STATUS_ITEM, max_length=1)

    def __str__(self):
        return str(self.batch)+"_"+str(self.file_name)
