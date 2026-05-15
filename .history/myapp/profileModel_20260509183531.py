from django.db import models

class FarmerProfile(models.Model):

    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    village = models.CharField(max_length=200)

    district = models.CharField(max_length=200)

    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name