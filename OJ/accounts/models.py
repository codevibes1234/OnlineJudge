from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExtendedUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    solvedProblems = models.CharField(max_length=20000)
    def __str__(self):
        return self.user.username

class OTP(models.Model):
    otp = models.CharField(max_length=8)