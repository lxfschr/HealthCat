from django.db import models
from django.conf import settings
import os

# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.
class Owner(models.Model):
  user = models.OneToOneField(User)
  zip_code=models.IntegerField(max_length=5, help_text='To compare your pet to other pets in your area.')
  photo = models.ImageField(upload_to="owner_photos", blank=True)
  
  def __unicode__(self):
    return self.user.username

class Bowl(models.Model):
    ip_address = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=20)
    owner = models.ForeignKey('Owner', related_name="bowl_owner")

    def __unicode__(self):
        return self.ip_address


"""
class Pet(models.Model):
    # one owner per pet
    owner = models.ForeignKey('Person', related_name='pet_owner')
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='pet_photos', blank=True)
    species = models.CharField(max_length=3,
        choices=(('C':'Cat'),('D':'Dog')))
    rfid = models.IntegerField(max_length=30, unique=True)
    statistics = models.OneToOneField('PetStats')
    schedule = models.ForeignKey('FoodSchedule')

# pet stats classification for all forms of health stats.
# a distinct class for organization. 
class PetStats(models.Model):
    weight = models.IntegerField(max_length=5)
    weightUnit = models.CharField(choices=(('KG':'Kilogram'),('LB':'Pound')))
    birthDay = models.DateField()
    age = models.IntegerField(max_length=5)
    activity = models.CharField(max_length=3,
        choices=(('M':'Male'),('F':'Female')))

    breed = models.ForeignKey('Breed')

    activity = models.CharField(max_length=3,
        choices=(('HIG':'High'),('LOW':'Low'),('MED':'Medium')))

    pregnant = models.BooleanField()
    nursing = models.BooleanField()
    sprayed = models.BooleanField()

    # other features concerning cats's health/performance
    # might be added here. 


class Breed(models.Model):
    name= models.CharField(max_length=50)

#Users can create multiple food schedules and save them to their
#profile, and assign them to pets. 
class FoodSchedule(models.Model):

    nameOfSchedule = models.CharField(max_length=20)
    maxAmountPerDay = models.IntegerField()
    def getScheduleQuerySet(self):
        return TimeAmountWindow.objects.filter(relatedSchedule=self)
        """