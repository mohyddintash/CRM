from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL)

    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # this is here because if an agent is deleted we still would want to track to what organisation his leads belong
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # Category is in quotes otherwise we need to place it at the top of this class
    category = models.ForeignKey(
        'Category', null=True, blank=True, related_name='leads', on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)

    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email}'


class Category(models.Model):
    # New, Contacted, Converted, Unconverted
    category_name = models.CharField(max_length=50, default='New')
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category_name}'

# Django Signals start here


def post_user_creation_signal(sender, instance, created, **kwargs):

    if created:
        # create a user porifle for the created user
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_creation_signal, sender=User)
