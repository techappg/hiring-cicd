from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def all_Samplepaper(request):
    all_sample=SamplePaper.objects.filter(user_id=request.user.company_id)
    return render(request,"all_sample_paper_record.html",locals())

@login_required(login_url="/")
def particular_sample_paper_details(request,id):
    print("newid",id)
    get_all = SamplePaper.objects.all()
    print(get_all)
    get_id=SamplePaper.objects.get(id=id)

    print(get_id.question.all())
    get_ques=get_id.question.all().order_by('ques_type')
    print(get_ques.order_by('ques_type'))


    return render(request, "particular_sample_paper_record.html", locals())

@login_required(login_url="/")
def get_sample_paper_details(request,id):
    print("coming")

    get_all = SamplePaper.objects.all()
    print(get_all)
    get_id=SamplePaper.objects.get(id=id)

    print(get_id.question.all())
    get_ques=get_id.question.all().order_by('ques_type')
    print(get_ques.order_by('ques_type'))


    return render(request, "record_sample.html", locals())


