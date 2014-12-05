from django.db import models
from django.conf import settings
import os

# User class for built-in authentication module
from django.contrib.auth.models import User

# Create your models here.
class Owner(models.Model):
  user = models.OneToOneField(User)
  zip_code=models.CharField(max_length=5, help_text='To compare your pet to other pets in your area.', blank=True)
  photo = models.ImageField(upload_to="owner_photos", blank=True)
  num_notifications = models.IntegerField(default=0)
  def __unicode__(self):
    return self.user.username

#connected bowls
class Bowl(models.Model):
    # ip_address = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=20)
    owner = models.ForeignKey('Owner', related_name="bowl_owner")
    pets = models.ManyToManyField('Pet')
    serial_number = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.serial_number

# bowls that used wanted to connect to , but
# the button on the bowl is not hit yet
class ConnectionPendingBowls(models.Model):
    uaBowl=models.ForeignKey('UnAssignedBowls',related_name='ua_bowl')
    owner=models.ForeignKey('Owner',related_name='cpbowl_owner')
    initTime = models.DateTimeField()
    name = models.CharField(max_length=20)

# all bowls serial and key table.
class UnAssignedBowls(models.Model):
    bowl_serial = models.CharField(max_length=100, unique=True)
    bowl_key = models.CharField(max_length=100)


class Pet(models.Model):
    # one owner per pet
    owner = models.ForeignKey('Owner', related_name='pet_owner')
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='pet_photos', blank=True)
    rfid = models.IntegerField(max_length=30, unique=True)

class FeedingInterval(models.Model):
    pet = models.ForeignKey('Pet', related_name="feeding_interval")
    start = models.TimeField()
    end = models.TimeField()
    amount = models.PositiveSmallIntegerField(max_length=5)

class Notification(models.Model):
    owner = models.ForeignKey('Owner', related_name="notification")
    bowl = models.ForeignKey('Bowl', related_name="bowl")
    date = models.DateTimeField()
    text = models.CharField(max_length=200)

class ConsumptionRecord(models.Model):
    pet = models.ForeignKey('Pet', related_name="consumption_pet")
    amount = models.PositiveSmallIntegerField(max_length=5)
    date = models.DateTimeField()
    duration = models.PositiveIntegerField()
    bowl = models.ForeignKey('Bowl', related_name="consumption_bowl")
    notification_text = models.CharField(max_length=200)

class BullyingRecord(models.Model):
    pet = models.ForeignKey('Pet', related_name="bullied_pet")
    bully = models.ForeignKey('Pet', related_name="bully_pet")
    date = models.DateTimeField()
    bowl = models.ForeignKey('Bowl', related_name="bully_bowl")
    notification_text = models.CharField(max_length=200)

class NewRFIDRecord(models.Model):
    rfid = models.CharField(max_length=32)
    date = models.DateTimeField()
    bowl = models.ForeignKey('Bowl', related_name="new_rfid_bowl")
    notification_text = models.CharField(max_length=200)

class RefilledBowlRecord(models.Model):
    amount = models.PositiveSmallIntegerField(max_length=5)
    date = models.DateTimeField()
    bowl = models.ForeignKey('Bowl', related_name="refilled_bowl")
    notification_text = models.CharField(max_length=200)

"""
# pet stats classification for all forms of health stats.
# a distinct class for organization. 
class PetStats(models.Model):
    species = models.CharField(max_length=3,
        choices=(('C':'Cat'),('D':'Dog')))
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