from django.db import models

# Create your models here.

class Pet(models.Model):
	rfid= models.IntegerField()
	schedule= models.ForeignKey('FoodSchedule',blank=True,null=True)

class FoodSchedule(models.Model):

    name=models.CharField(max_length=20)
    maxAmountPerDay = models.IntegerField(null=True,blank=True)
    def getScheduleQuerySet(self):
        return TimeAmountWindow.objects.filter(relatedSchedule=self)

class TimeAmountWindow(models.Model):

    timeOpen = models.TimeField()
    timeClose = models.TimeField()
    amount = models.IntegerField(null=True,blank=True)
    relatedSchedule= models.ForeignKey('FoodSchedule')