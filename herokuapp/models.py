from django.db import models

# Create your models here.


class State(models.Model):
    last_update = models.DateTimeField(auto_now_add=True)


class Suspects(models.Model):
    username = models.CharField(max_length=50)
    num_ask = models.IntegerField(default=0)
