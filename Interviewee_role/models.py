from django.db import models

from Product_owner_role.models import User
from django.contrib.postgres.fields import ArrayField

import uuid

class Interviwee_Profile(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    phone_no = models.CharField(max_length=12,null=True,blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    cv = models.FileField(upload_to='',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)
    link_time=models.DateField(null=True,blank=True)
    language = models.CharField(max_length=255, default="")
    level = models.CharField(max_length=255, default="")
    interviwer_mail=models.EmailField(max_length=200, blank=True, null=True)
    link=models.UUIDField( default=uuid.uuid4,null=True,blank=True)
    sample_paper=models.CharField(max_length=255, null=True,blank=True)
    addedby_company=models.ForeignKey('company_role.Company_Profile',on_delete=models.CASCADE,null=True,blank=True)
    addedby_superuser=models.BooleanField(default=False, null=True, blank=True)




# Create your models here.
