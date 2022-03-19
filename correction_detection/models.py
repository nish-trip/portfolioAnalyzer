from django.db import models

# Create your models here.
class Users(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

# <QuerySet [{'id': 1, 'email': 'tripathynishant@gmail.com', 'password': 'abc'}]>
# {'id': 1, 'email': 'tripathynishant@gmail.com', 'password': 'abc'}