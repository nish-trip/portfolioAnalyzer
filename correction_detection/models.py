from django.db import models

class Stocks(models.Model):
    name = models.CharField(max_length=30, null=True)
    owner_id = models.IntegerField() # owner ID references the ID of the users table