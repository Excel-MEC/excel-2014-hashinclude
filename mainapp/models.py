from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    id=models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    college = models.CharField(max_length=50)
    totalscore = models.FloatField(default=0)
    totalsolutions = models.IntegerField(default=0)
    totalsubmissions = models.IntegerField(default=0)

class Problem(models.Model):
    id=models.AutoField(primary_key=True)    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    score = models.FloatField(default=0)
    avgtime = models.FloatField(default=0)
    timelimit = models.FloatField(default=0)
    difficulty = models.CharField(max_length=50)
    
class Submission(models.Model):
    id=models.AutoField(primary_key=True)
    playerid = models.ForeignKey(Player)
    problemid = models.ForeignKey(Problem)
    status = models.CharField(max_length=50,default='Queued')
    errormessage = models.CharField(max_length=50)
    score = models.FloatField(default=0)
    language = models.CharField(max_length=50)
    timetaken = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
         
class Solution(models.Model):
    id=models.AutoField(primary_key=True)
    playerid = models.ForeignKey(Player)
    problemid = models.ForeignKey(Problem)
    submissionid = models.ForeignKey(Submission)
    score = models.FloatField(default=0)
    
    class Meta:
        unique_together = (("playerid", "problemid","submissionid"),)