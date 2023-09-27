from distutils.command.upload import upload
from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import FilePathField




class Bids(models.Model):
    bid = models.IntegerField(blank=True, null=True)

class Comments(models.Model):
    comment = models.CharField(max_length=100)

class Listings(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='files', null=True, blank=True)
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comments, blank=True)
    
class User(AbstractUser):
    watchlist = models.ManyToManyField(Listings, blank=True)
    bids = models.ManyToManyField(Bids, blank=True)
    created_listing = models.ManyToManyField(Listings, blank=True, related_name="created_listings")