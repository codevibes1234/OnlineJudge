from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=25)
    statement = models.CharField(max_length=20000)
    def __str__(self):
        return f'{self.title}'
    
class Solution(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    verdict = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.problem.title} {self.user.username}'

class TestCase(models.Model):
    input = models.CharField(max_length=10000)
    output = models.CharField(max_length=10000)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.problem.title}'
    