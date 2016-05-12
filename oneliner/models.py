from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Organization(models.Model):
    name = models.CharField(max_length=250)
    url = models.URLField()
    size = models.CharField(
        max_length=1,
        choices=(
            ('A', 'Less than 50 full-time employees'),
            ('B', 'Between 50-100 full-time employees'),
            ('C', 'Greater than 100 full-time employees'),
        ),
        default="?")

    budget = models.CharField(
        max_length=1,
        choices=(
            ('A', 'Less than $10'),
            ('B', 'Less than $100'),
            ('C', 'Less than $500'),
            ('D', 'More than $500'),
        ),
        default="?")

    pageviews = models.CharField(
        max_length=1,
        choices=(
            ('A', 'Less than 10,000'),
            ('B', 'Less than 50,000'),
            ('C', 'Less than 1 million'),
            ('D', 'More than 1 million'),
        ),
        default="?"


    )



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    def __str__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
