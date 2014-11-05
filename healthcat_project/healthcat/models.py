from django.db import models
from django.conf import settings
import os

# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
  user = models.OneToOneField(User)
  first_name = models.CharField(max_length=42, default="")
  last_name = models.CharField(max_length=42, default="")
  phone_number=models.IntegerField("Phone Number",max_length=15,blank=True)
  zip_code=models.IntegerField(max_length=5)
  profile_pic = models.ImageField(upload_to="profile_pictures", blank=True)
  def __unicode__(self):
    return self.user.username

