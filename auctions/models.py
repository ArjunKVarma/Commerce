from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listings(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null= True, blank=True)
    price= models.IntegerField(default=0)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    photo = models.CharField(max_length=2000)
    date = models.DateTimeField()
    highest_bidder = models.CharField(max_length=100, default="None")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, default= "others",verbose_name="")

    def __str__(self):
        return f"{self.id} : {self.name}, {self.price}, {self.date}"

class bids(models.Model):
    value = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    Listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, blank=True)
    


class Comments(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null = True)
    Listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True)
    Comment = models.CharField(max_length=600)

    
    def __str__(self):
        return f'{self.User}: {self.Comment}'