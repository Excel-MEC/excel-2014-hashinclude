from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Problem(models.Model):
    id=models.AutoField(primary_key=True)    
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    score = models.FloatField(default=0)
    timelimit = models.FloatField(default=1)
    difficulty = models.CharField(max_length=50)

class Player(models.Model):
    id=models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default='N/A')
    fbuserid = models.CharField(max_length=50,default='N/A')
    college = models.CharField(max_length=50,default='N/A')
    totalscore = models.FloatField(default=0)
    totalsolutions = models.IntegerField(default=0)
    totalsubmissions = models.IntegerField(default=0)
    problems_viewed = models.ManyToManyField(Problem,blank=True,null=True)
    lastsolutiontime = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        ordering = ["-totalscore","lastsolutiontime"]

class PlayerProblemViewTime(models.Model):
    playerid = models.ForeignKey(Player)
    problemid = models.ForeignKey(Problem)
    viewtime = models.DateTimeField(auto_now=True)

class Submission(models.Model):
    id=models.AutoField(primary_key=True)
    playerid = models.ForeignKey(Player)
    problemid = models.ForeignKey(Problem)
    status = models.CharField(max_length=50,default='Processing')
    score = models.FloatField(default=0)
    language = models.CharField(max_length=50)
    timetaken = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)
    safe = models.BooleanField(default=True)
