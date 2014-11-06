from django.db import models

# Create your models here.

class Pet(models.Model):
	rfid= models.IntegerField()
	schedule= models.ForeignKey('FoodSchedule')

class FoodSchedule(models.Model):

    nameOfSchedule = models.CharField(max_length=20)
    maxAmountPerDay = models.IntegerField()
    def getScheduleQuerySet(self):
        return TimeAmountWindow.objects.filter(relatedSchedule=self)

class TimeAmountWindow(models.Model):

    timeOpen = models.TimeField()
    timeClose = models.TimeField()
    amount = models.IntegerField(blank=True)
    relatedSchedule= models.ForeignKey('FoodSchedule')

