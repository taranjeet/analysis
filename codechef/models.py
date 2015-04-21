from django.db import models

# Create your models here.
class Easy(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=500)

class Medium(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=500)

class Hard(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=500)

class Challenge(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=500)

class Peer(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=500)

class School(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=500)

class College(models.Model):
    code=models.CharField(max_length=200)
    name=models.CharField(max_length=500)
    date=models.CharField(max_length=50)

class User(models.Model):
    name=models.CharField(max_length=500)
    username=models.CharField(max_length=200)
    collegename=models.CharField(max_length=500)

# class CampusChapter(models.Model):
#     name = models.CharField(max_length = 1000)
#     code = models.CharField(max_length = 100, primary_key=True)
#     college = models.CharField(max_length = 1000)
#     avgLong = models.FloatField()
#     avgCookOff = models.FloatField()
#     avgLunchtime = models.FloatField()
#     thisAvgLong = models.FloatField()
#     thisAvgCookOff = models.FloatField()
#     thisAvglunchtime = models.FloatField()
#     #createdAt = models.DateTimeField(default = None)
'''
It may happen that the models will be changed for the tables that contain the DateTimeField
'''
# class CrawlingStats(models.Model):
#     lastCrawledDate = models.DateTimeField()


class PageCount(models.Model):
    sort_newest_count=models.IntegerField()


class Contest(models.Model):
    contest=models.CharField(max_length=50)
    code=models.IntegerField()
    month=models.IntegerField()
    year=models.IntegerField()
