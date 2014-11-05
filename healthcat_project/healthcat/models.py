from django.db import models
from django.conf import settings
import os

# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.
class Owner(models.Model):
  user = models.OneToOneField(User)
  zip_code=models.IntegerField(max_length=5)
  photo = models.ImageField(upload_to="owner_photos", blank=True)
  def __unicode__(self):
    return self.user.username

