from django.db import models

# Create your models here.


class TestModel(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    colour = models.CharField(max_length=200)

    class Meta:
        unique_together = ["name", "colour"]
