from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Organization(models.Model): #All information about an organization that uses One-liner
    
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
        default="?")

    def __str__(self):
        return self.name

class Services(models.Model): #Table for all the services that One-liner offers
    name = models.CharField(max_length=250)
    price = models.CharField(max_length = 3000, blank=True, null=True)
    performance = models.CharField(max_length = 3000, blank=True, null=True  )
    privacy = models.CharField(max_length=3000, blank=True, null=True)
    organizations = models.ManyToManyField(Organization, blank=True, null=True) #Organizations can have many services and each service can be used by many organizations

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #Should we keep this as null=true, blank=true Or make sure that every
    #person is associated with an organization? 
    #Should we use on_delete cascade for the foreign key here? Which means if the organization in the
    #table is deleted, all the people using it will be deleted?
    organization = models.ForeignKey(Organization, blank=True, null=True) #Many users can belong to an organization
    def __str__(self):
        return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
