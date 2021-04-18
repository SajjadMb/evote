from django.db import models
from django.utils import timezone
from account.models import ElectionUser
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Election(models.Model):
    elector = models.ForeignKey(
        ElectionUser,
        on_delete=models.CASCADE
        )
    election_name = models.CharField(max_length=250)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    description = models.CharField(blank=True, max_length=500)
    election_url = models.SlugField(blank=True, max_length=255)

    class Meta:
        get_latest_by = 'end_time'


class Candidate(models.Model):
    firstname = models.CharField(blank=True, max_length=255)
    lastname = models.CharField(blank=True, max_length=255)
    email=models.EmailField(blank=True)
    description = models.CharField(blank=True, max_length=500)
    profile_photo = models.ImageField(upload_to='../media/pic_folder/candidate_photo', default='../media/pic_folder/None/anonymous.jpg', blank=True)
    f_election= models.ForeignKey(Election, on_delete=models.CASCADE)


class Voter(models.Model):
    f_election = models.ForeignKey(Election,on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    national_code = models.CharField(blank=True, max_length=15)


class Vote(models.Model):
    f_voter = models.OneToOneField(
        Voter,
        on_delete=models.CASCADE,
        blank=True
    )
    choice = ArrayField(models.CharField(max_length=255), size=10)
