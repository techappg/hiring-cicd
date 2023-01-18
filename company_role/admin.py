from django.contrib import admin

from Interviewee_role.models import Interviwee_Profile
from company_role.models import Company_Profile,IntervieweeTestDetails,Hr_Profile

admin.site.register(Company_Profile)
admin.site.register(Interviwee_Profile)
admin.site.register(IntervieweeTestDetails)
admin.site.register(Hr_Profile)
# Register your models here.
