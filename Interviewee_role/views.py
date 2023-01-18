from django.db.models import Q
from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from Sample_Paper.models import SamplePaper,Test_Record,Question
from Product_owner_role.models import TaskLanguage, TaskLevel,User
from .models import Interviwee_Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from company_role.models import *
from django.template.loader import render_to_string
import datetime
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives


@login_required(login_url="/")
def interviwee_register(request):
    all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
                                                     Q(editby_company_id=request.user.company_id), is_active=True).values_list("name")
    all_level = TaskLevel.objects.filter(Q(addedby_superuser=True) |
                                         Q(addedby_company_id=request.user.company_id), is_active=True).values_list("name")
    if request.method == "POST":

            


                get_sample_paper = request.POST.get("sample_paper1")
                mail = request.POST['email']
                print("anju",mail)
                x=request.user.email
                print("deepp",x)

                interviwee_Profile = Interviwee_Profile.objects.create(name=request.POST['name'],
                                                                 phone_no=request.POST['phone_no'],
                                                                 email=mail,
                                                                 cv=request.FILES["cv_file"],
                                                                 link_time=request.POST["expire"],
                                                                 password=request.POST["interviwee_Password"],
                                                                 language=request.POST.get('task_language'),
                                                                 level=request.POST.get('level_task'),
                                                                 addedby_company_id=request.user.company_id,
                                                                 interviwer_mail=x,
                                                                 sample_paper=get_sample_paper)

                print("this")
                if request.user.is_superuser==True:
                    print("super")
                    interviwee_Profile.addedby_superuser = True
                    interviwee_Profile.save()

                else:
                    print("company")
                get_sample_paper=request.POST.get("sample_paper1")
                request.session["get_sample_paper"]= get_sample_paper

                request.session["interviwee_Profile"]=interviwee_Profile.pk
                interviwee_detail=Interviwee_Profile.objects.get(id= request.session["interviwee_Profile"])
                Company_name=Company_Profile.objects.get(id=interviwee_detail.addedby_company_id)
                print(interviwee_detail.language)
                taskLanguage = TaskLanguage.objects.get(name=interviwee_detail.language.lower())
                print(taskLanguage)
                taskLevel = TaskLevel.objects.get(name=interviwee_detail.level.lower())
                # value=SamplePaper.objects.get(id=get_sample_paper)
                # print(value.public_url)
                # print("df")

                interviwee_detail=IntervieweeTestDetails.objects.create(interviewer_id=request.user.id,interviewee=interviwee_Profile,test_id=request.session["get_sample_paper"])
                request.session["interviwee_detail"]=interviwee_detail.pk

                subject = 'you have  been invited for the test'
                text_content = 'This is an important message.'
                html_content = render_to_string("email.html",
                 {
                     "interviwee_Profile":interviwee_Profile,
                     
                     "Company_name":Company_name

                 })
                msg = EmailMultiAlternatives(subject, text_content, "hiringvisiontrek@gmail.com", [mail])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                added=True
    return render(request, 'interviwe.html', locals())


@login_required(login_url="/")
def dummy(request):

    all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
                                                     Q(editby_company_id=request.user.company_id), is_active=True).values_list("name",)
    print(all_task_languages)
    language=request.GET.get("language")
    level=request.GET.get("level")
    print(language)
    print(level)
    if TaskLanguage.objects.filter(name=language.lower(), editby_company_id=request.user.company_id).exists():
        get_language = TaskLanguage.objects.get(name=language.lower(),
                                                editby_company_id=request.user.company_id)

    else:
        get_language = TaskLanguage.objects.get(name=language.lower())

    if TaskLevel.objects.filter(name=level.lower(), addedby_company_id=request.user.company_id).exists():
        get_level = TaskLevel.objects.get(name=level.lower(), addedby_company_id=request.user.company_id)

    else:
        get_level = TaskLevel.objects.get(name=level.lower())

    # get_language=TaskLanguage.objects.get(name= language.lower(),editby_company_id=request.user.company_id)
    # get_level=TaskLevel.objects.get(name= level.lower(),addedby_company_id=request.user.company_id)
    # print(get_language)
    if request.user.is_superuser:
       sample_paper = SamplePaper.objects.filter(language_id= get_language,level_id= get_level,user_id=request.user.company_id)
       for i in sample_paper:
           print(i.title)
    else:
        sample_paper = SamplePaper.objects.filter(Q(language_id=get_language, level_id=get_level),Q(user_id=request.user.company_id)|Q(user_id=1))
        for i in sample_paper:
            print(i.title)
    print(sample_paper)
    print("anjuuu")


    return render(request, 'language_dropdown_list_options.html',locals())


from datetime import date
def link_detail(request,id):
    # value = SamplePaper.objects.get(id=request.COOKIES["sample_id"])
    # duration_time = value.duration
    # duration_time = int(duration_time)
    today = date.today()
    get_intervieww=Interviwee_Profile.objects.get(link=id)
    value = SamplePaper.objects.get(id=get_intervieww.sample_paper)
    y=value.question.all().count()
    duration_time = value.duration
    duration_time = int(duration_time)
    print(get_intervieww.added_on)
    check_link=IntervieweeTestDetails.objects.get(interviewee=get_intervieww.id)
    response=render(request, 'interview_confirm.html', locals())
    response.set_cookie('get_sample_paper',get_intervieww.id)
    # usr=User.objects.get(company_id=get_intervieww.addedby_company_id)
    response.set_cookie('compony_mail',get_intervieww.interviwer_mail)
    response.set_cookie('sample_id',get_intervieww.sample_paper)


    if check_link.is_completed_by_computer==False and check_link.is_completed==False and  today <= get_intervieww.link_time:
        request.session['interviwer'] =id

        print(get_intervieww.email)
        print(id)
        return response
    else:
        return render(request, 'noteligible.html', locals())

def get_paper(request):
            current_date = datetime.datetime.now()
            print("this is get method")
            interviwe_record = IntervieweeTestDetails.objects.get(interviewee_id=request.COOKIES["get_sample_paper"])

            interviwe_record.started_at = current_date
            interviwe_record.save()

            value = SamplePaper.objects.get(id=request.COOKIES["sample_id"])

            duration_time = value.duration
            duration_time = int(duration_time)
            all_ques = value.question.all()[:1]
            all_count = value.question.all().count()
            print(all_count)
            myList = {}
            for i in all_ques:
                if i.option_type:
                    
                    img1=i.ques_images1
                    img2=i.ques_images2
                    img3=i.ques_images3
                    img4=i.ques_images4
                request.session["running_quest_id"]=i.id
                print(i.id)
                print("this is session")
                myList[i.ques] = i.ques_option
                break

            request.session["count"] = 1
            request.session['all_ques_count'] = all_count

            return render(request, 'step_3.html', locals())


def submit_answer(request):

    if request.method == "POST":
        x = request.POST.get("auto_submit_form", "off")
        yy = request.POST.get("next", "off")


        question = request.POST["question"]
        answer = request.POST.get("answer")
        print(answer)
        print("anju",request.session.get("running_quest_id"))
        ques = Question.objects.get(id=request.session["running_quest_id"])

        interviwe_record = IntervieweeTestDetails.objects.get(interviewee_id=request.COOKIES["get_sample_paper"])

        data = Test_Record.objects.create(sample_paper_id=request.COOKIES["sample_id"],
                                          question_id=ques.id, interviewee_TestDetails=interviwe_record,
                                          answer=answer)

        count = int(request.session["count"])
        print("count", count)
        all_qust = int(request.session["all_ques_count"])

        if all_qust == count:
            
            
            interviwe_record.is_completed=True
            interviwe_record.completed_at=datetime.datetime.now()
            interviwe_record.save()
            usr = request.session["interviwer"]
            interviweee = Interviwee_Profile.objects.get(link=usr)
            test_record_user=IntervieweeTestDetails.objects.get(interviewee_id=interviweee)
            print(interviweee.addedby_company)

            subject = 'Test Submission link'
            text_content="submittt"
            html_content = render_to_string("test_record_email.html",
            {
                "interviweee": interviweee,
                "test_record_user": test_record_user

            })

            # message = f"{interviweee.name} has been completed their task \n http://38.242.219.47:8006/interviwee/{test_record_user.id}"
            msg = EmailMultiAlternatives(subject, text_content, "hiringvisiontrek@gmail.com", [request.COOKIES.get('compony_mail')])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # email = EmailMessage(subject, message, "kaulneerja1@gmail.com",[request.COOKIES.get('compony_mail')])
            # email.send()
            response=render(request, 'submit.html', locals())
            # response.delete_cookie('get_sample_paper')
            # usr=User.objects.get(company_id=get_intervieww.addedby_company_id)
            # response.delete_cookie('compony_mail')
            # response.delete_cookie('sample_id')

            return response

        if x=="True":
            interviwe_record.is_completed_by_computer= True
            interviwe_record.completed_at = datetime.datetime.now()
            interviwe_record.save()
            usr = request.session["interviwer"]
            interviweee = Interviwee_Profile.objects.get(link=usr)
            test_record_user = IntervieweeTestDetails.objects.get(interviewee_id=interviweee)
            print(interviweee.addedby_company)
            subject = 'Test Submission link'
            text_content = "submittt"
            html_content = render_to_string("test_record_email.html",
            {
                "interviweee": interviweee,
                "test_record_user": test_record_user

            })

            # message = f"{interviweee.name} has been completed their task \n http://38.242.219.47:8006/interviwee/{test_record_user.id}"
            msg = EmailMultiAlternatives(subject, text_content, "hiringvisiontrek@gmail.com",
                                         [request.COOKIES.get('compony_mail')])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # subject = 'Email verification message'
            #
            # message = f"{interviweee.name} has been completed their task \n http://38.242.219.47:8006/interviwee/{test_record_user.id}"
            #
            # email = EmailMessage(subject, message, "kaulneerja1@gmail.com", [request.COOKIES.get('compony_mail')])
            # email.send()
            response = render(request, 'thanku.html', locals())
            response.delete_cookie('get_sample_paper')
            # usr=User.objects.get(company_id=get_intervieww.addedby_company_id)
            response.delete_cookie('compony_mail')
            response.delete_cookie('sample_id')

            return response




        request.session["count"] = count + 1

        value = SamplePaper.objects.get(id=request.COOKIES["sample_id"])
        duration_time = value.duration
        duration_time = int(duration_time)
        all_ques = value.question.all().order_by('ques_type')[count:count + 1]
        print(all_ques)

        myList = {}
        for i in all_ques:
            if i.option_type:
                img1 = i.ques_images1
                img2 = i.ques_images2
                img3 = i.ques_images3
                img4 = i.ques_images4
            request.session["running_quest_id"] = i.id
            myList.clear()
            myList[i.ques] = i.ques_option
            break

        return render(request, 'step_3.html', locals())

@login_required(login_url="/")
def interviwee_task_details(request,type):
  print('user::',request.user.id)
  if type=="all":
    if request.user.is_HR:
        company=User.objects.get(company_id=request.user.company_id,is_HR=False)
        print(company.id)
        interviwee_record = IntervieweeTestDetails.objects.filter(Q(interviewer_id=request.user.id)|Q(interviewer_id=company.id)).order_by('id')

    else:
        if Hr_Profile.objects.filter(added_by_id=request.user.company_id).exists():
           company = User.objects.filter(company_id=request.user.company_id, is_HR=True)
           for i in company:
               print("anju",i.id)
               interviwee_record = IntervieweeTestDetails.objects.filter(Q(interviewer_id=request.user.id)|
                                                                  Q(interviewer_id=i.id)).order_by('id')

        else:
            interviwee_record = IntervieweeTestDetails.objects.filter(interviewer_id=request.user.id).order_by('id')

  elif type == "start_time":
        if request.user.is_HR:
            print("niidfidif")
            company = User.objects.get(company_id=request.user.company_id, is_HR=False)
            print("hey",company)
            print(company.id)
            interviwee_record = IntervieweeTestDetails.objects.filter(
                Q(interviewer_id=request.user.id,started_at__isnull = False) | Q(interviewer_id=company.id,started_at__isnull = False)).order_by('id')

        else:
            if Hr_Profile.objects.filter(added_by_id=request.user.company_id).exists():
                company = User.objects.filter(company_id=request.user.company_id, is_HR=True)
                for i in company:
                    print(i.id)
                interviwee_record = IntervieweeTestDetails.objects.filter(Q(interviewer_id=request.user.id,started_at__isnull = False) |
                                                                          Q(interviewer_id=i.id,started_at__isnull = False)).order_by('id')

            else:
                interviwee_record = IntervieweeTestDetails.objects.filter(interviewer_id=request.user.id,started_at__isnull = False).order_by('id')
  return render(request, 'all_interviwee_record.html', locals())



def particular_interviweee_detail(request,id):
    get_interviwee = IntervieweeTestDetails.objects.get(id=id)
    current_user=User.objects.get(id=get_interviwee.interviewer_id)
    all_ques = get_interviwee.test.question.all()
    test_record=Test_Record.objects.filter(interviewee_TestDetails_id=get_interviwee.id)
    ans=Test_Record.objects.filter(interviewee_TestDetails_id=get_interviwee.id,question_id__ques_type=1)
    test_record_id=Test_Record.objects.filter(interviewee_TestDetails_id=get_interviwee.id,question_id__ques_type=1).values_list('question_id',flat=True)
    db_ques = Question.objects.filter(id__in=test_record_id,ques_type=1).order_by("id")

    count = 0
    print(test_record_id)
    print(db_ques)
    # print(ans)
    # print(db_ques)
    for y,x in zip(db_ques,ans):
        print(y.ans,x.answer)
        if y.ans==x.answer:
            count=count+1

    print("finalcount",count)

    if request.method == "POST":
        status = request.POST.get('pass')
        print("sdbbdb")
        print("now",status)
        if status=="true":
            get_interviwee.status = "Pass"
            get_interviwee.send_email = "True"
            get_interviwee.save()
            subject = 'you have  been invited for the next round'
            text_content = 'This is an important message.'
            html_content = render_to_string("pass_status.html",
                                            {
                                                "get_interviwee": get_interviwee,
                                                "current_user":current_user,

                                            })
            msg = EmailMultiAlternatives(subject, text_content, "hiringvisiontrek@gmail.com", [get_interviwee.interviewee.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            added = True


        elif status=="false":
            get_interviwee.status = "fail"
            get_interviwee.send_email = "True"
            get_interviwee.save()
            subject = 'Better luck for next time!Thank You'
            text_content = 'This is an important message.'
            html_content = render_to_string("fail_status.html",
                                            {
                                                "get_interviwee": get_interviwee,
                                                "current_user": current_user,

                                            })
            msg = EmailMultiAlternatives(subject, text_content, "hiringvisiontrek@gmail.com",
                                         [get_interviwee.interviewee.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            added = True



    
    return render(request, 'particular_interviwee_detail.html', locals())



    


