from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=25)
    statement = models.CharField(max_length=20000)
    def __str__(self):
        return f'{self.title}'
    
class Solution(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.FileField(upload_to='submissions',blank=True,null=True)
    verdict = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    tcspassed = models.CharField(max_length=20000,null=True)
    compilationError = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.problem.title} {self.user.username}'

class TestCase(models.Model):
    input = models.TextField(null=True,blank=True)
    output = models.TextField(null=True,blank=True)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.problem.title}'

@receiver(post_delete, sender=Solution)
def delete_file_on_submission_delete(sender, instance, **kwargs):
    if instance.code:
        instance.code.delete(save=False)