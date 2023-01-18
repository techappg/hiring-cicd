from django.contrib import admin

from Sample_Paper.models import Question,SamplePaper,Test_Record,Question_Type

admin.site.register(Question)
admin.site.register(SamplePaper)
admin.site.register(Test_Record)
admin.site.register(Question_Type)

# Register your models here.
