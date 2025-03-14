from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    participant_name = models.CharField(max_length=100, blank=False, null=False)
    participant_email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    participant_phone = models.CharField(max_length=20, blank=False, null=False)
    participant_dateOfBirth = models.DateField(blank=False, null=False)
    participant_skills = models.JSONField(default=list, blank=False, null=False)
    participant_linkedin = models.URLField(max_length=200, blank=False, null=False)
    participant_github = models.URLField(max_length=200, blank=False, null=False)
    participant_portfolio = models.URLField(max_length=200, blank=True, null=True)
    participant_haveParticipated = models.BooleanField(default=False, blank=True)
    participant_status = models.CharField(max_length=20, default='Pending', null=True, blank=True)
    participant_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.participant_name
    

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100 , unique=True,  blank=False, null=False)
    team_leader = models.ForeignKey(Participant, on_delete=models.CASCADE ,  blank=False, null=False)
    team_project_name = models.CharField(max_length=100, null=True, blank=True)
    team_project_description = models.TextField(max_length=500, null=True, blank=True)
    team_project_links = models.JSONField(default=list, null=True, blank=True)


class AdminManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Admins must have an email address")
        
        email = self.normalize_email(email)
        admin = self.model(email=email, name=name)
        admin.set_password(password)  
        admin.save(using=self._db)
        return admin

    def create_superuser(self, email, name, password=None):
        admin = self.create_user(email, name, password)
        admin.is_staff = True
        admin.is_superuser = True
        admin.save(using=self._db)
        return admin

class Admin(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=True) 

    objects = AdminManager()  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Stat(models.Model):
    id = models.AutoField(primary_key=True)
    total_participants = models.IntegerField(default=0)
    total_teams = models.IntegerField(default=0)
    refused_participants = models.IntegerField(default=0)
    accepted_participants = models.IntegerField(default=0)
    all_participants = models.IntegerField(default=0)
    all_teams = models.IntegerField(default=0)

