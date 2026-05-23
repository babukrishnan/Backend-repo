from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    phone = models.CharField(
        max_length=20,
        # unique=True
    )

    village = models.CharField(max_length=200)

    district = models.CharField(max_length=200)

    farming = models.CharField(
        max_length=200,
        blank=True,
        null= True
    )

    land_size = models.CharField(
        max_length=100,
        null=True,      
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    is_completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name