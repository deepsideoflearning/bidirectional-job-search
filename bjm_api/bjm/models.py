from django.db import models

class BJM(models.Model):
    name = models.CharField(max_length=50)
    paradigm = models.CharField(max_length=50)

    def __str__(self):
        return self.name