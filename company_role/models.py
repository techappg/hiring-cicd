from django.db import models
import uuid
from uuid import uuid4

from Interviewee_role .models import *
from Product_owner_role.models import *
from Sample_Paper.models import SamplePaper


class Company_Profile(models.Model):
    company_Name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_phone_no = models.CharField(max_length=12, null=True, blank=True)
    company_email = models.EmailField()
    company_Password = models.CharField(max_length=255)
    company_state = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)



class OTP(models.Model):
    otp=models.IntegerField()
    user=models.ForeignKey('Product_owner_role.User',on_delete=models.CASCADE,null=True,blank=True)
    added_on = models.DateField(auto_now_add=True)







class IntervieweeTestDetails(models.Model):
    interviewer=models.ForeignKey('Product_owner_role.User',on_delete=models.DO_NOTHING,null=True,blank=True)
    interviewee = models.ForeignKey('Interviewee_role.Interviwee_Profile',on_delete=models.DO_NOTHING,null=True,blank=True)
    started_at = models.DateTimeField(null=True,blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True,blank=True)
    test=models.ForeignKey(SamplePaper,on_delete=models.DO_NOTHING,null=True,blank=True)
    answer=models.CharField(max_length=255,null=True,blank=True)
    is_completed_by_computer = models.BooleanField(default=False)
    status=models.CharField(max_length=15,default="pending")
    remarks = models.TextField(default="")
    send_email=models.BooleanField(default=False)

    #
    #

    # def __str__(self):
    #     return f"{self.interviewer}"



class Hr_Profile(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    added_by=models.ForeignKey('company_role.Company_Profile',on_delete=models.DO_NOTHING,null=True,blank=True)



