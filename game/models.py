from django.db import models


class User(models.Model):
    id = models.AutoField("ID", primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30, )
