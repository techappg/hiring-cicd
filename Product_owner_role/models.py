from django.contrib.auth.models import AbstractUser
from django.db import models

from company_role.models import *


class User(AbstractUser):
    user_mobile = models.CharField(max_length=10, null=True)
    is_HR=models.BooleanField(default=False,null=True,blank=True)
    is_company=models.BooleanField(default=False,null=True,blank=True)
    company=models.ForeignKey(Company_Profile,on_delete=models.DO_NOTHING,null=True,blank=True)

class TaskLanguage(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)
    logo=models.ImageField(null=True,blank=True)
    editby_superuser=models.BooleanField(default=False,null=True,blank=True)
    editby_company=models.ForeignKey('company_role.Company_Profile',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

class TaskLevel(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)
    addedby_superuser = models.BooleanField(default=False, null=True, blank=True)
    addedby_company = models.ForeignKey('company_role.Company_Profile', on_delete=models.CASCADE, null=True, blank=True)

    #
    def __str__(self):
        return self.name
    #

