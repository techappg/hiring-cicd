
from django.db import models

from company_role.models import *
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField

class Question_Type(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name

class Question(models.Model):
    language = models.ForeignKey('Product_owner_role.TaskLanguage',on_delete=models.DO_NOTHING,null=True,blank=True)
    level = models.ForeignKey('Product_owner_role.TaskLevel', on_delete=models.DO_NOTHING,null=True,blank=True)
    ques_type = models.ForeignKey('Question_Type', on_delete=models.CASCADE, null=True, blank=True)
    ques=RichTextField(blank=True,null=True)
    ques_option = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    ques_images1 = models.ImageField(upload_to="images", null=True, blank=True)
    ques_images2 = models.ImageField(upload_to="images", null=True, blank=True)
    ques_images3 = models.ImageField(upload_to="images", null=True, blank=True)
    ques_images4 = models.ImageField(upload_to="images", null=True, blank=True)
    ans = models.TextField()
    option_type = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)
    editby_superuser = models.BooleanField(default=False, null=True, blank=True)
    addedby_company = models.ForeignKey('company_role.Company_Profile', on_delete=models.CASCADE, null=True, blank=True)
    order=models.IntegerField(null=True,blank=True,default=0)




import uuid
class SamplePaper(models.Model):

    public_url = models.UUIDField( default=uuid.uuid4,null=True,blank=True)
    language = models.ForeignKey('Product_owner_role.TaskLanguage', on_delete=models.CASCADE,null=True,blank=True)
    level = models.ForeignKey('Product_owner_role.TaskLevel', on_delete=models.CASCADE,null=True,blank=True)
    ques_type = models.ForeignKey('Question_Type',on_delete=models.CASCADE,null=True,blank=True)
    question= models.ManyToManyField('Question',null=True,blank=True)
    title=models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    is_publish=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    added_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey('company_role.Company_Profile', on_delete=models.CASCADE, null=True, blank=True)






class Test_Record(models.Model):
    sample_paper = models.ForeignKey(SamplePaper,on_delete=models.CASCADE,null=True,blank=True)
    interviewee_TestDetails = models.ForeignKey('company_role.IntervieweeTestDetails',on_delete=models.CASCADE,null=True,blank=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True)
    answer=models.TextField(null=True,blank=True)
