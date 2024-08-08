from django.db import models

class AuctionItem(models.Model):
    photo = models.ImageField(upload_to='images/',blank=True, null=True)
    name  = models.CharField(max_length=100)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)


def  __str__(self):
    return self.name

