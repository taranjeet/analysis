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