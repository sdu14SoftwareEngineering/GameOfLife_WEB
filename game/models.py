from django.db import models


class User(models.Model):
    id = models.AutoField("ID", primary_key=True)
    username = models.CharField(max_length=30)
    win = models.IntegerField()
    fail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'game_user'
