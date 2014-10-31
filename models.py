from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):

    user=models.OneToOneField(User)

    #basic information of every user
    firstName= models.CharField("First Name",max_length=50) 
    lastName= models.CharField("Last Name",max_length=50)
    bio= models.CharField("Bio",max_length=300)
    dateOfBirth=models.DateField("Date of Birth (MM/DD/YYYY) ")
    phone=models.IntegerField("Phone",max_length=15,blank=True)
    proPic= models.ImageField(upload_to='proPicsFolder', blank=True)


class Pet(models.Model):

    # there could currently be only one owner to a pet.
    owner = models.ForeignKey('Person', related_name = 'petOwner')
    moderators = models.ManyToMany('Person',related_name='petMods')

    profilePic= models.ImageField(upload_to='petProfilePic',blank=True)
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=100)

    rfid= models.IntegerField(max_length=30)

    statistics = models.OneToOneField('PetStats')

    schedule = models.ForeignKey('FoodSchedule')

# pet stats classification for all forms of health stats.
# a distinct class for organization. 
class PetStats(models.Model):

    weight = models.IntegerField(max_length=5)
    age = models.IntegerField(max_length=5)
    breed = models.ForeignKey('Breed')

    activity = models.CharField(max_length=3,
        choices=(('HIG':'High'),('LOW':'Low'),('MED':'Medium')))

    # other features concerning cats's health/performance
    # might be added here. 



#Users can create multiple food schedules and save them to their
#profile, and assign them to pets. 
class FoodSchedule(models.Model):

    nameOfSchedule = models.CharField(max_length=20)
    maxAmountPerDay = models.IntegerField()
    def getScheduleQuerySet(self):
        return TimeWindow.objects.filter(relatedSchedule=self)


class TimeWindow(models.Model):

    timeOpen = models.TimeField()
    timeClose = models.TimeField()
    amount = models.IntegerField(blank=True)
    relatedSchedule= models.ForeignKey('FoodSchedule')

class Bowl(models.Model):

    owner = models.ForeignKey('Person', related_name="bowlOwner")
    moderators = models.ManyToMany('Person',related_name="bowlMods")

    petsToServe = models.ManyToMany('Bowl')

    maxCapacity = models.IntegerField(max_length=5)
    currentCapacity = models.IntegerField(max_length=5)


class Food(models.Model):
    brandName = models.CharField(max_length=50)
    company  = models.ForeignKey('Company')
    logo= models.ImageField(upload_to='food', blank=True)

    def getAverageRating():
        pass


class Company(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='companyLogo',blank=True)

class FoodReview (models.Model):
    writer = models.ForeignKey('Person') 
    food = models.ForiegnKey('Food')
    content = models.CharField(max_length = 1000)

class FoodSpecs(models.Model):
    WETFOOD = 'WET'
    DRYFOOD = 'DRY'
    FOODTYPE = ((WETFOOD, 'Wet Food'),(DRYFOOD, 'Dry Food') )

    foodtype = models.CharField(max_length=5, choices = FOODTYPE,
            default=DRYFOOD)

    # add more specs here abour the food .



