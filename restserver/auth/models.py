from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.contrib.auth.models import User

class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100, unique=True)
    # should we have a state choices set, if yes, add them here, or we can have them hardcoded in frontend
    state = models.CharField(max_length=100, unique=True)
    # currently country is India so we dont ask for now. In future may have to ask

class StudyField(models.Model):
    name = models.CharField(max_length=100, unique=True)
    shortname = models.CharField(max_length=10, unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.OneToOneField(College, on_delete=models.SET_NULL, null=True)
    fieldofstudy = models.OneToOneField(StudyField, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10, null=True)
    YEAR_CHOICES = []
    #graduation year is max 5 years from date of registration
    for r in range((datetime.datetime.now().year), (datetime.datetime.now().year+5)):
        YEAR_CHOICES.append((r,r))

    graduation_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    provider = models.CharField(max_length=20, null=True)

    def savedata(self, data):
        self.graduation_year = data["graduation_year"]
        self.phone = data["phone"]
        self.filedofstudy = StudyField.objects.get(pk=data["fieldofstudy"])
        self.college = College.objects.get(pk=data["college"])
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#Create CodingProfile
#Create EnglishProfile
#Create ReadingProfile
#Create InterviewProfile
#Create TechnicalProfile
#Create ForumProfile
#Create other profiles as needed like TeamProfile etc.

