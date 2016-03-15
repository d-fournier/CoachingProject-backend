from django.db import models
from django.contrib.auth.models import User
from level.models import Level


def user_directory_path(instance, filename):
    return 'profile_pictures/{0}_{1}'.format(instance.id, filename)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=50)
    birthdate = models.DateField(blank=True, null=True)
    isCoach = models.BooleanField(default=False)
    city = models.CharField(max_length=50)
    description = models.TextField(max_length=400, blank=True, default='')
    levels = models.ManyToManyField(Level, blank=True, default=[])
    picture = models.ImageField(upload_to=user_directory_path, default=None, null=True, blank=True)

    def __str__(self):
        return self.displayName
