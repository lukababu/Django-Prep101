from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Marketer(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    phone       = models.CharField(max_length=14)

    def __str__(self):
        return self.user.get_full_name()

class Manager(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    phone       = models.CharField(max_length=14)

    def __str__(self):
        return self.user.get_full_name()

class Locker(models.Model):
    number      = models.IntegerField()
    location    = models.CharField(max_length=10)
    combination = models.CharField(max_length=9)

    def __str__(self):
        return self.location + str(self.number)

class Shift(models.Model):
    handout_type            = models.CharField(max_length=20)
    location                = models.CharField(max_length=10)
    time                    = models.DateTimeField()
    class_name              = models.CharField(max_length=16)

    # Relationships
    locker                  = models.ForeignKey(Locker)
    lead_marketer           = models.ForeignKey(Marketer, related_name='lead_marketer', null=True, blank=True)
    marketers               = models.ManyToManyField(Marketer, related_name='marketers', blank=True)
    manager                 = models.ForeignKey(Manager, null=True, blank=True)

    # Constraints
    max_marketers           = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.class_name

class Expenses(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    amount      = models.FloatField()
    receipt     = models.BooleanField()
    date        = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.class_name