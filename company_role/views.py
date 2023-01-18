from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q,Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
import pandas as pd
from django.contrib.auth.decorators import login_required
import random
from django.http import FileResponse
from django.contrib import messages
from .tokens import account_activation_token
from django.template.loader import render_to_string
from Product_owner_role.models import User, TaskLanguage, TaskLevel
from company_role.models import *
from company_role.models import Company_Profile, Hr_Profile,IntervieweeTestDetails
from Interviewee_role.models import Interviwee_Profile
from Sample_Paper.models import SamplePaper,Question_Type,Question
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives

@login_required(login_url="/")
def dashboard_index(request):
    try:
       if request.user.is_superuser:
           language=TaskLanguage.objects.filter(editby_superuser=True).count()
           company=Company_Profile.objects.all().count()
           active_company=Company_Profile.objects.filter(is_active=True).count()
           deactive_company=Company_Profile.objects.filter(is_active=False).count()
           hr=Hr_Profile.objects.filter(added_by=request.user.company_id).count()
           sample_paper = SamplePaper.objects.filter(user_id=request.user.company_id).count()
           interviewee=Interviwee_Profile.objects.filter(addedby_superuser=True).count()
           interviewee_test_record = IntervieweeTestDetails.objects.filter(interviewer_id=request.user.company_id,started_at__isnull = False).count()

       elif request.user.is_company:
           language = TaskLanguage.objects.filter(Q(editby_company_id=request.user.company_id)|Q(editby_superuser=True)).count()

           hr = Hr_Profile.objects.filter(added_by=request.user.company_id).count()
           interviewee = Interviwee_Profile.objects.filter(addedby_company=request.user.company_id).count()
           print("u",interviewee)
           sample_paper = SamplePaper.objects.filter(user_id=request.user.company_id).count()
           if Hr_Profile.objects.filter(added_by_id=request.user.company_id).exists():
               company = User.objects.get(company_id=request.user.company_id, is_HR=True)
               interviewee_test_record = IntervieweeTestDetails.objects.filter(Q(interviewer_id=request.user.id,started_at__isnull=False) |
                                                                         Q(interviewer_id=company.id,started_at__isnull=False)).order_by('id').count()

           else:
               interviewee_test_record = IntervieweeTestDetails.objects.filter(interviewer_id=request.user.id,started_at__isnull=False).order_by('id').count()


           # interviewee_test_record = IntervieweeTestDetails.objects.filter(interviewer_id=request.user.company_id,started_at__isnull = False).count()
           # print("i",interviewee_test_record)

       elif request.user.is_HR:
           interviewee = Interviwee_Profile.objects.filter(addedby_company=request.user.company_id).count()
           print(interviewee)

           company = User.objects.get(company_id=request.user.company_id, is_HR=False)
           print(company.id)
           interviewee_test_record = IntervieweeTestDetails.objects.filter(
               Q(interviewer_id=request.user.id,started_at__isnull=False) | Q(interviewer_id=company.id,started_at__isnull=False)).count()


           # interviewee_test_record = IntervieweeTestDetails.objects.filter(interviewer_id=request.user.company_id,started_at__isnull=False).count()
           # print("ishu",interviewee_test_record)




       return render(request, "dashboard.html", locals())
    except:
        return redirect("/")




def Admin_login(request):
        print("hghj")
        if request.method == "POST":
                username_or_email = request.POST['username_or_email']
                print(username_or_email)
                password = request.POST['password']
                print(password)
                is_email=False
                found=False
                for i in username_or_email:
                    if i=="@":
                        is_email=True
                if is_email:
                    if not User.objects.filter(email=username_or_email).exists():
                        username_not_found = True
                    else:
                        found = True
                        username=User.objects.get(email=username_or_email).username

                if not is_email:
                    if not User.objects.filter(username=username_or_email).exists():
                        username_not_found = True
                    else:
                        found=True
                        username = User.objects.get(username=username_or_email).username
                if found:


                    user= auth.authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        print("login")
                        return redirect('/dashboard_index')
                    else:
                        invalid=True

                        print("invalid credentials")
        else:
            print("not login")
        return render(request, 'profile_login.html', locals())

@login_required(login_url="/")
def get_language(request):
    if request.user.is_superuser == True:
        if request.method == "POST":
            if TaskLanguage.objects.filter(name=request.POST['name'].lower(),editby_superuser=True).exists():
                Language=True
            else:
                language = TaskLanguage.objects.create(name=request.POST['name'].lower(), editby_superuser=True)

                print(language)

    elif request.user.is_company == True:
        if request.method == "POST":
            if TaskLanguage.objects.filter(Q(name=request.POST['name'].lower(), editby_company_id=request.user.company_id)|Q(name=request.POST['name'].lower(),editby_superuser=True)).exists():
                Language = True
            else:
                language = TaskLanguage.objects.create(name=request.POST['name'].lower(), editby_company_id=request.user.company_id)
                print(language)

    else:
        print("jdsj")

    all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
                                              Q(editby_company_id=request.user.company_id), is_active=True)
    print("valuess")
    print( all_task_languages)



    return render(request, 'view_all_language.html', locals())


@login_required(login_url="/")
def get_level(request):
    if request.user.is_superuser == True:
        if request.method == "POST":
            if TaskLevel.objects.filter(name=request.POST['name'],addedby_superuser=True).exists():
                tasklevel=True
            else:
                language = TaskLevel.objects.create(name=request.POST['name'].lower(), addedby_superuser=True)
                print(language)

    elif request.user.is_company == True:
        if request.method == "POST":
            if TaskLevel.objects.filter(Q(name=request.POST['name'],addedby_company_id=request.user.company_id)|Q(name=request.POST['name'],addedby_superuser=True)).exists():
                tasklevel=True
            else:
                language = TaskLevel.objects.create(name=request.POST['name'].lower(), addedby_company_id=request.user.company_id)
                print(language)



    all_level = TaskLevel.objects.filter(Q(addedby_superuser=True) |
                                              Q(addedby_company_id=request.user.company_id), is_active=True)


    return render(request, 'inbuilt_level.html', locals())



@login_required(login_url="/")
def get_allcompanies(request):
    added=False
    if request.method == "POST":
        company_Name = request.POST['company_Name']
        company_address = request.POST['company_address']
        company_phone_no = request.POST['company_phone_no']
        company_email = request.POST["company_email"]
        company_Password = request.POST['company_Password']
        company_state = request.POST['company_state']
        if User.objects.filter(
                Q(username=request.POST['company_Name']) | Q(email=request.POST["company_email"])).exists():
            print("dndmmdmdgd")
            all = True
            email=False
            name=False
            if User.objects.filter(email=request.POST["company_email"]).exists():
                print("email true")
                email = True
            if User.objects.filter(username=request.POST['company_Name']).exists():
                print("name true")
                name = True

        else:
            company_profile = Company_Profile.objects.create(company_Name=request.POST['company_Name'],
                                                             company_address=request.POST['company_address'],
                                                             company_phone_no=request.POST['company_phone_no'],
                                                             company_email=request.POST["company_email"],
                                                             company_Password=request.POST['company_Password'],
                                                             company_state=request.POST['company_state'])
            print(company_profile)

            request.session['company_Profile'] = company_profile.pk
            get = request.session['company_Profile']
            x = Company_Profile.objects.get(id=company_profile.pk)
            user = User.objects.create(company=company_profile, username=company_profile.company_Name,user_mobile=company_profile.company_phone_no,email=company_profile.company_email,password=company_profile.company_Password, is_company=True)
            user.set_password(x.company_Password)
            user.save()
            added=True

    if request.user.is_superuser == True:
        all_companies=Company_Profile.objects.all()
        print(all_companies)
    else:
        print("error")
    return render(request, 'all_companies.html', locals())

@login_required(login_url="/")
def view_particular_company_details(request,id):
    get_value=Company_Profile.objects.get(id=id)

    return render(request, 'particular_company_detail.html', locals())

@login_required(login_url="/")
def update_particular_company_details(request,id):
    get_value=Company_Profile.objects.get(id=id)
    if request.method == "POST":
        get_value.company_Name= request.POST["company_Name"]
        get_value.company_phone_no = request.POST["company_phone_no"]
        get_value.company_email = request.POST["company_email"]
        get_value.company_state= request.POST["company_state"]
        get_value.company_address= request.POST["company_address"]

        get_value.save()
        user = User.objects.get(company_id=get_value.id)
        user.email = company_detail.company_email
        user.user_mobile = company_detail.company_phone_no
        user.save()
        return redirect("/get_allcompanies")

    return render(request, 'update_company_detail.html', locals())



@login_required(login_url="/")
def decativate_company(request,id):
    get=Company_Profile.objects.get(id=id)
    get.is_active=False
    get.save()
    user=User.objects.get(username=get.company_Name)
    user.is_active=False
    user.save()
    return redirect("/get_allcompanies")

@login_required(login_url="/")
def activate_company(request,id):
    get=Company_Profile.objects.get(id=id)
    get.is_active=True
    get.save()
    user=User.objects.get(username=get.company_Name)
    user.is_active=True
    user.save()
    return redirect("/get_allcompanies")



@login_required(login_url="/")
def add_questions(request):
        print("jjdj")
        all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
                                              Q(editby_company_id=request.user.company_id), is_active=True).values_list("name")
        all_level = TaskLevel.objects.filter(Q(addedby_superuser=True) |
                                              Q(addedby_company_id=request.user.company_id), is_active=True).values_list("name")
        all_ques_type= Question_Type.objects.filter(is_active=True).values_list('name')

        all_ques_ans = Question.objects.all()
        print(all_ques_ans)
        if request.method == "POST":
          if request.user.is_superuser==True:

                languge=request.POST['task_language'].lower()
                level=request.POST['level_task'].lower()
                ques_type=request.POST['ques_type'].lower()
                option_type=request.POST['exampleRadios']

                taskLanguage = TaskLanguage.objects.get(
                    Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge, editby_superuser=True))
                taskLevel = TaskLevel.objects.get(
                    Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level, addedby_superuser=True))
                # taskLanguage = TaskLanguage.objects.get(name=languge)
                # taskLevel = TaskLevel.objects.get(name=level)
                # ques_Type = Question_Type.objects.get(name=ques_type)

                max_order = Question.objects.filter(language=taskLanguage, level=taskLevel).aggregate(max_order=Max('order'))
                print(max_order)
                if  max_order.get('max_order'):
                    max_order = max_order.get('max_order')
                else:
                    max_order=0

                if ques_type=="mcq"and option_type=="text" :
                    value1=request.POST['value1']
                    print("i",value1)
                    value2=request.POST['value2']
                    value3=request.POST['value3']
                    value4=request.POST['value4']
                    total_values=[value1,value2,value3,value4]
                    taskLanguage = TaskLanguage.objects.get(
                        Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge,
                                                                                       editby_superuser=True))
                    taskLevel = TaskLevel.objects.get(
                        Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level,
                                                                                      addedby_superuser=True))
                    ques_Type= Question_Type.objects.get(name=ques_type)
                    print( ques_Type)
                    question= Question.objects.create(language=taskLanguage,
                                                      level=taskLevel,
                                                      ques=request.POST['ques'],
                                                      ques_type=ques_Type,
                                                      ans=request.POST['select_answer'],
                                                      ques_option=total_values,
                                                      editby_superuser=True,
                                                      order=max_order+1)
                    print(question.ques_option)

                elif ques_type=="mcq"and option_type=="image" :
                    value1 = request.FILES['a']
                    value2 = request.FILES['b']

                    value3 = request.FILES['c']
                    value4 = request.FILES['d']
                    anss = request.POST['select_answer']
                    print("image",anss)
                    taskLanguage = TaskLanguage.objects.get(
                        Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge,
                                                                                       editby_superuser=True))
                    taskLevel = TaskLevel.objects.get(
                        Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level,
                                                                                      addedby_superuser=True))
                    ques_Type = Question_Type.objects.get(name=ques_type)
                    print(ques_Type)
                    question = Question.objects.create(language=taskLanguage, level=taskLevel,
                                                       ques=request.POST['ques'], ques_type=ques_Type,

                                                       ques_images1=value1,
                                                       ques_images2=value2,
                                                       ques_images3=value3,
                                                       ques_images4=value4,
                                                       option_type=True,
                                                       editby_superuser=True, order=max_order + 1)

                    answer=Question.objects.get(id=question.id)
                    if anss=="A":
                        answer.ans=question.ques_images1
                        answer.save()
                    elif anss=="B":
                        answer.ans=question.ques_images2
                        answer.save()
                    elif anss=="C":
                        answer.ans=question.ques_images3
                        answer.save()
                    elif anss=="D":
                        answer.ans=question.ques_images4

                        answer.save()






                else:
                    taskLanguage = TaskLanguage.objects.get(
                        Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge,
                                                                                       editby_superuser=True))
                    taskLevel = TaskLevel.objects.get(
                        Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level,
                                                                                      addedby_superuser=True))
                    ques_Type= Question_Type.objects.get(name=ques_type)
                    print( ques_Type)
                    question= Question.objects.create(language=taskLanguage,level=taskLevel,ques=request.POST['ques'],ques_type=ques_Type,editby_superuser=True,order=max_order+1)

                # return redirect("/create_sample_paper")
                added = True
          elif request.user.is_company==True:

                languge = request.POST['task_language'].lower()
                level = request.POST['level_task'].lower()
                ques_type = request.POST['ques_type'].lower()
                option_type = request.POST['exampleRadios']
                taskLanguage = TaskLanguage.objects.get(Q(name=languge,editby_company_id=request.user.company_id)|Q(name=languge,editby_superuser=True))
                taskLevel = TaskLevel.objects.get(Q(name=level,addedby_company_id=request.user.company_id)|Q(name=level,addedby_superuser=True))
                ques_Type = Question_Type.objects.get(name=ques_type)

                max_order=Question.objects.filter(language=taskLanguage, level=taskLevel).aggregate(max_order=Max('order'))
                print(max_order)
                if max_order.get('max_order'):
                    max_order = max_order.get('max_order')
                else:
                    max_order = 0


                if ques_type=="mcq"and option_type=="text" :
                    value1 = request.POST['value1']
                    print("i u",value1)
                    value2 = request.POST['value2']
                    value3 = request.POST['value3']
                    value4 = request.POST['value4']
                    total_values = [value1, value2, value3, value4]
                    print(total_values)
                    taskLanguage = TaskLanguage.objects.get(
                        Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge,
                                                                                       editby_superuser=True))
                    taskLevel = TaskLevel.objects.get(
                        Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level,
                                                                                      addedby_superuser=True))
                    ques_Type = Question_Type.objects.get(name=ques_type)
                    print(ques_Type)
                    question = Question.objects.create(language=taskLanguage, level=taskLevel, ques=request.POST['ques'],
                                                       ques_type=ques_Type, ques_option=total_values,ans=request.POST['select_answer'], addedby_company_id=request.user.company_id,order=max_order+1)

                elif ques_type=="mcq"and option_type=="image" :
                    value1 = request.FILES['a']
                    value2 = request.FILES['b']
                    value3 = request.FILES['c']
                    value4 = request.FILES['d']
                    anss = request.POST['select_answer']
                    print("answer is ",anss)
                    taskLanguage = TaskLanguage.objects.get(
                        Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge,
                                                                                       editby_superuser=True))
                    taskLevel = TaskLevel.objects.get(
                        Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level,
                                                                                      addedby_superuser=True))
                    ques_Type = Question_Type.objects.get(name=ques_type)
                    print(ques_Type)
                    question = Question.objects.create(language=taskLanguage, level=taskLevel,
                                                       ques=request.POST['ques'],
                                                       ques_type=ques_Type,
                                                       ques_images1=value1,
                                                       ques_images2=value2,
                                                       ques_images3=value3,
                                                       ques_images4=value4,
                                                       option_type=True,
                                                       addedby_company_id=request.user.company_id, order=max_order + 1)

                    answer = Question.objects.get(id=question.id)
                    if anss == "A":
                        answer.ans = question.ques_images1
                        answer.save()
                    elif anss == "B":
                        answer.ans = question.ques_images2
                        answer.save()
                    elif anss == "C":
                        answer.ans = question.ques_images3
                        answer.save()
                    elif anss == "D":
                        answer.ans = question.ques_images4

                        answer.save()


                else:
                    taskLanguage = TaskLanguage.objects.get(
                        Q(name=languge, editby_company_id=request.user.company_id) | Q(name=languge,
                                                                                       editby_superuser=True))
                    taskLevel = TaskLevel.objects.get(
                        Q(name=level, addedby_company_id=request.user.company_id) | Q(name=level,
                                                                                      addedby_superuser=True))
                    ques_Type= Question_Type.objects.get(name=ques_type)
                    print( ques_Type)
                    question= Question.objects.create(
                        language=taskLanguage,
                        level=taskLevel,
                        ques=request.POST['ques'],
                        ques_type=ques_Type,
                        addedby_company_id=request.user.company_id,
                        order=max_order+1,
                    )
                added = True
                # return redirect("/create_sample_paper")

        else:
            print("exit")
        return render(request, 'add_ques_ans.html', locals())


@login_required(login_url="/")
def create_sample_paper(request):

        all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
                                              Q(editby_company_id=request.user.company_id), is_active=True).values_list("name")
        print(all_task_languages)
        all_level = TaskLevel.objects.filter(Q(addedby_superuser=True) |
                                              Q(addedby_company_id=request.user.company_id), is_active=True).values_list("name")
        # all_ques = Question.objects.filter(is_active=True).values_list('ques')
        # all_ques_type = Question_Type.objects.filter(is_active=True).values_list('name')

        if request.method == "POST":
            language=request.POST.get('task_language').lower()
            request.session['language']=language

            print(language)
            level=request.POST.get('level_task').lower()
            print(level)
            request.session["level"]=level
            print(request.user.company_id)
            taskLanguage = TaskLanguage.objects.get(Q(name=language,editby_company=request.user.company_id)|Q(name=language,editby_superuser=True))
            print(taskLanguage)
            taskLevel = TaskLevel.objects.get(Q(name=level,addedby_company_id=request.user.company_id)|Q(name=level,addedby_superuser=True))
            print(taskLevel)
            # question1 =Question .objects.filter(Q(language=taskLanguage,level=taskLevel,editby_superuser=True) | Q(addedby_company_id=request.user.company_id))
            question1 =Question .objects.filter(Q(language=taskLanguage,level=taskLevel,addedby_company_id=request.user.company_id)|Q(language=taskLanguage,level=taskLevel,editby_superuser=True))
            print(question1)

            return render(request, 'get_sample_paper.html', locals())
        else:
            print("exit")

        return render(request, 'add_sample_paper.html', locals())








@login_required(login_url="/")
def new_value(request):
    if request.method == "POST":
        if  TaskLanguage.objects.filter(name=request.session['language'], editby_company_id=request.user.company_id).exists():
             taskLanguage = TaskLanguage.objects.get(name=request.session['language'],editby_company_id=request.user.company_id)

        else:
            taskLanguage = TaskLanguage.objects.get(name=request.session['language'],editby_superuser=True)


        if TaskLevel.objects.filter(name=request.session['level'],addedby_company_id=request.user.company_id).exists():
            taskLevel = TaskLevel.objects.get(name=request.session['level'], addedby_company_id=request.user.company_id)

        else:
            taskLevel = TaskLevel.objects.get(name=request.session['level'],addedby_superuser=True)
        sample=SamplePaper.objects.create(language=taskLanguage,level=taskLevel,user_id=request.user.company_id)
        request.session["sample"] = sample.pk
        question = Question.objects.filter(language=taskLanguage, level=taskLevel)

        texxt=[]
        for i in question:
            ques_type = request.POST.get(f"box_{i.pk}", "off")
            print(ques_type)
            if ques_type == "off":
                pass
            else:
                print("on checkbox ",ques_type)
                ques = Question.objects.get(id=ques_type)
                if ques.ques_type_id==1:
                   sample.question.add(ques)
                   sample.save()
                else:
                   texxt.append(ques.id)
        logical=[]
        for ques in texxt:
            question = Question.objects.get(id=ques)
            if question.ques_type_id == 2:
                sample.question.add(question)
                sample.save()
            else:
                logical.append(question.id)

        for ques in logical:
            question = Question.objects.get(id=ques)
            if question.ques_type_id == 3:
                sample.question.add(question)
                sample.save()

        print("text",texxt)
        print("logical",logical)







        return redirect("/add_duration")

        return HttpResponse("BDF")


@login_required(login_url="/")
def add_duration(request):
    if request.method=="POST":
        title=request.POST["title"]
        print(title)
        duration=request.POST["duration"]
        print(duration)
        sample1=SamplePaper.objects.get(id= request.session["sample"])
        print(sample1)
        sample1.title=title
        sample1.duration=duration
        sample1.save()
        return redirect("/display_sample_paper")

    return render(request, 'duration.html', locals())




@login_required(login_url="/")
def get_sample(request):
    all_sample=" "
    print("request",request.method)
    all_sample = SamplePaper.objects.filter(Q(user_id=request.user.company_id) |
                                            Q(user_id=1))
    print("get", all_sample)

    all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
                                                     Q(editby_company_id=request.user.company_id), is_active=True).values_list(
        "name")
    all_level = TaskLevel.objects.filter(Q(addedby_superuser=True) |
                                         Q(addedby_company=request.user.company_id), is_active=True).values_list("name")
    if request.method=="GET":
    
        # all_sample = SamplePaper.objects.filter(Q(user=request.user) |
        #                                                  Q(user_id=1))
        # print("get",all_sample)
        #
        # all_task_languages = TaskLanguage.objects.filter(Q(editby_superuser=True) |
        #                                                  Q(editby_company=request.user), is_active=True).values_list(
        #     "name")
        print(all_task_languages)
        all_level = TaskLevel.objects.filter(Q(addedby_superuser=True) |
                                             Q(addedby_company_id=request.user.company_id), is_active=True).values_list("name")

        # if request.method=="POST":
    else:
        print(request.POST['task_language'])
        print(request.POST['level_task'])
        taskLanguage = TaskLanguage.objects.get(name=request.POST['task_language'].lower())
        print(taskLanguage)
        taskLevel = TaskLevel.objects.get(name=request.POST['level_task'].lower())
        print(taskLevel)

        all_sample=SamplePaper.objects.filter(Q(language=taskLanguage,level=taskLevel),Q(user_id=request.user.company_id)|Q(user_id=1))
        print("post",all_sample)



        # return render(request, 'overall_sample_paper.html',locals())

    return  render(request,"get_all_sample_paper.html",locals())



@login_required(login_url="/")
def view_sample_paper(request,public_url):
    c=SamplePaper.objects.get(public_url=public_url)
    print(c)
    all_ques=c.question.all()
    print(all_ques)
    print("hlloo")
    print(all_ques)


    return render(request, 'view_ques.html', locals())


def companyRegister(request):
        print("company")
        if request.method == "POST":
            company_Name = request.POST['company_Name']
            company_address = request.POST['company_address']
            company_phone_no = request.POST['company_phone_no']
            company_email = request.POST["company_email"]
            company_Password = request.POST['company_Password']
            company_state = request.POST['company_state']
            otp = random.randint(1000, 9999)

            if User.objects.filter(
                    Q(username=request.POST['company_Name']) | Q(email=request.POST["company_email"])).exists():
                print("dndmmdmdgd")
                all = True
                email = False
                name = False
                if User.objects.filter(email=request.POST["company_email"]).exists():
                    print("email true")
                    email = True
                if User.objects.filter(username=request.POST['company_Name']).exists():
                    print("name true")
                    name = True
            else:
                subject = "verify otp"
                message = f"Hi {company_Name}\n We're happy you signed up with our portal.\n Please verify your otp {otp} for login process\n  Regards\n Visiontrek Communications"




                reply_to_list = [company_email]
                email = EmailMessage(subject, message, 'hiringvisiontrek@gmail.com', reply_to_list)
                email.send()

                companyprofile = Company_Profile.objects.create(company_Name=request.POST['company_Name'],
                                                                      company_address=request.POST['company_address'],
                                                                      company_phone_no=request.POST['company_phone_no'],
                                                                      company_email=request.POST["company_email"],
                                                                      company_Password=request.POST['company_Password'],
                                                                      company_state=request.POST['company_state'],
                                                                              )




                request.session['company_Profile']=companyprofile.pk
                get=request.session['company_Profile']
                # x=Company_Profile.objects.get(id=companyprofile.pk)
                user=User.objects.create(company=companyprofile,username=companyprofile.company_Name,email=companyprofile.company_email ,user_mobile=companyprofile.company_phone_no,password=companyprofile.company_Password,is_company=True,is_active=False)
                user.set_password(companyprofile.company_Password)
                request.session["email"]=user.email
                user.save()
                create_otp=OTP.objects.create(otp=otp,user=user)
                return redirect("/otp")

        return render(request, 'company_profile.html', locals())


def otp_verify(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        if "email" in request.session:
          use = User.objects.get(email=request.session["email"])
        else:
            if "email" in request.POST:
                mail = request.POST["email"]
                use = User.objects.get(email=mail)
            else:
                mail=True
                return render(request, "validotp.html", locals())

        company = Company_Profile.objects.get(company_email=use.email)
        print(company.company_Password)
        print(use.password)
        print(use.username)
        get_otp=OTP.objects.get(user_id=use.id)
        if int(otp) == get_otp.otp:
            use.is_active = True
            use.save()
            request.session['user'] = use.username
            request.session['uid'] = use.email
            user = auth.authenticate(username=use.username, password=company.company_Password)

            print(user)
            if user is not None:
                auth.login(request, user)
                print("login")
                return redirect('/dashboard_index')

        else:
            messages.error(request, 'please enter a valid otp')
    return render(request, "validotp.html", locals())


@login_required(login_url="/")
def Hr_profile(request):
    x=request.user.company_id
    if request.method == "POST":
        hrfirst_name=request.POST['first_name']
        hrlast_name=request.POST['last_name']
        hr_phoneno=request.POST['hr_phoneno']
        hr_email=request.POST['hr_email']
        hr_password=request.POST['hr_password']
        # if User.objects.filter(
        #         Q(username=request.POST['hrfirst_name']) | Q(email=request.POST["hr_email"])).exists():
        #
        #     email = False
        #     name = False
        if User.objects.filter(email=request.POST["hr_email"]).exists():
                print("email true")
                email = True
            # if User.objects.filter(username=request.POST['hr_name']).exists():
            #     print("name true")
            #     name = True

                return render(request, 'HR_profile.html', locals())

        else:
                print(request.user.company)
                print("useeeee",x)
                print(Company_Profile.objects.get(id=request.user.company_id))
                hrprofile =Hr_Profile.objects.create(first_name=request.POST['first_name'],
                                                                last_name=request.POST['last_name'],
                                                                phone_no=request.POST['hr_phoneno'],
                                                                email=request.POST['hr_email'],
                                                                password=request.POST["hr_password"],
                                                                added_by_id=request.user.company_id)

                get=hrprofile.email
                name=request.user.username
                print("now user",request.user.id)
                user = User.objects.create(is_HR=True, username=hrprofile.email,email=hrprofile.email,password=hrprofile.password,user_mobile=hrprofile.phone_no,company_id=x)
                user.set_password(hrprofile.password)
                user.save()
                subject = 'Your Credentials'
                text_content = 'This is an important message.'
                html_content = render_to_string("Hr_info.html",
                                                {
                                                    "hrprofile": hrprofile,
                                                     "name":name

                                                })
                msg = EmailMultiAlternatives(subject, text_content, "hiringvisiontrek@gmail.com", [get])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                added = True
                name=False
                email=False
                return render(request, 'HR_profile.html', locals())
    return render(request, 'HR_profile.html', locals())

@login_required(login_url="/")
def all_hr_record(request):
    hr_record = Hr_Profile.objects.filter(Q(added_by=request.user.company_id))
    
    return render(request, 'all_hr_record.html', locals())


@login_required(login_url="/")
def view_particular_hr_detail(request,id):
    get_hr=Hr_Profile.objects.get(id=id)

    return render(request, 'particular_hr_detail.html', locals())

@login_required(login_url="/")
def update_particular_hr_details(request,id):
    update_hr = Hr_Profile.objects.get(id=id)
    a = User.objects.get(email=update_hr.email)

    if request.method == "POST":

        update_hr.first_name= request.POST["hr_name"]
        update_hr.last_name= request.POST["last_name"]
        update_hr.email = request.POST["hr_email"]
        update_hr.phone_no= request.POST["hr_phone_no"]

        if a.email != request.POST["hr_email"]:
           if User.objects.filter(email=request.POST["hr_email"]).exists():
                print("email true")
                email = True
                return render(request, 'update_hr_detail.html', locals())


        print(a.email)
        a.email=request.POST["hr_email"]
        a.username=request.POST["hr_email"]
        a.user_moile=request.POST["hr_phone_no"]
        a.save()
        update_hr.save()
        hr_updated=True
        return redirect("/all_hr")

    return render(request, 'update_hr_detail.html', locals())





def pie_chart(request):
    labels = []
    data = []

    queryset = Interviwee_Profile.objects.filter(language="Python").count()
    labels.append(queryset)
    data.append(queryset)

    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
    })


def view_company(request, type):
    is_active = True
    print('type::', type)
    if type == "active":
        is_active = True
    else:
        is_active = False
    get_company=Company_Profile.objects.filter(is_active=is_active)

    print(get_company)
    return render(request, 'companies.html', locals())


def detail_company(request,id):
    get_value = Company_Profile.objects.get(id=id)

    return render(request, 'company_detail.html', locals())


@login_required(login_url="/")
def upload_file(request):
    try:
        if request.method=="POST":
                get_file=request.FILES['file']
                print(get_file)
                data = pd.read_excel(get_file)
                df = pd.DataFrame(data)
                print(df)
                df=df.fillna('')
                for index, row in df.iterrows():
                    language = row["department"].strip()
                    level = row["level"].strip()
                    ques_type = row["ques_type"].strip()
                    ques = row["question"]
                    option1 = row["option1"]
                    option2 = row["option2"]
                    option3 = row["option3"]
                    option4 = row["option4"]
                    ans = row["correct_ans"]
                    print(language)
                    total_values = [option1, option2, option3, option4]
                    taskLanguage = TaskLanguage.objects.get(name=language)
                    print(taskLanguage)
                    taskLevel = TaskLevel.objects.get(name=level)
                    ques_Type = Question_Type.objects.get(name=ques_type)
                    print(ques_Type)
                    max_order = Question.objects.filter(language=taskLanguage, level=taskLevel).aggregate(
                        max_order=Max('order'))
                    print(max_order)
                    if max_order.get('max_order'):
                        max_order = max_order.get('max_order')
                    else:
                        max_order = 0
    
                    if Question.objects.filter(Q(language=taskLanguage,
                                            level=taskLevel,
                                            ques=ques,
                                            ques_type=ques_Type,
                                            editby_superuser=True)|Q(language=taskLanguage,
                                            level=taskLevel,
                                            ques=ques,
                                            ques_type=ques_Type,addedby_company_id=request.user.company_id)).exists():
                        print("hello")
                        continue
                    elif(ques_type=="text" or ques_type=="logical"):
                            question = Question.objects.create(language=taskLanguage,
                                                               level=taskLevel,
                                                               ques=ques,
                                                               ques_type=ques_Type,
                                                               order=max_order + 1)
                    else:
                        print("notttt")
                        question=Question.objects.create(language=taskLanguage,
                                                    level=taskLevel,
                                                    ques=ques,
                                                    ques_type=ques_Type,
                                                    ans=ans,
                                                    ques_option=total_values,
                                                    order=max_order + 1)
    
                    if request.user.is_superuser:
                        question.editby_superuser = True
                        question.save()
                        added=True
                    elif request.user.is_company:
                        question.addedby_company_id=request.user.company_id
                        question.save()
                        added=True
                    print(question.ques_option)
    
        return render(request, "upload_file.html", locals())
    except Exception as e:
         exception=True
         return render(request, "upload_file.html", locals())
        

def password_reset(request):
    print("nnnngnn")
    if request.method == "POST":
            email = request.POST['email']
            print(email)
            if not User.objects.filter(email=email).exists():
                print(email)
                email_not_found=True
            else:

                qs = User.objects.get(email=email)
                print(qs)
                qs.is_active = False
                qs.save()

                current_site = get_current_site(request)
                mail_subject = 'password reset link has been sent to your email id'
                message = render_to_string('password_reset_mail.html', {
                    'user': qs,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(qs.pk)),
                    'token': account_activation_token.make_token(qs),
                })


                email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                email.send()
                messages.success(request, 'Please confirm your email address for Password reset process!')
                return redirect("/password_forgot")



    return render(request, 'password_forgot_form.html',locals())




def reset(request, uidb64, token):

    if request.method == 'POST':



            print("tryof rest")
            uid = force_str(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(id=uid)
            print("hello",user)


            a=request.POST['password']
            b=request.POST['password1']
            if a==b:

                print("form valid of reset")
                user.set_password(request.POST['password1'])
                user.is_active = True
                user.save()
                messages.success(request,'Password has been successfully updated!')
                return redirect("/")

            else:
                print("errror")
                messages.error(request,'Your Passwords does not match')



    return render(request, 'password_reset_form.html', locals())

@login_required(login_url="/")
def profile_logout(request):
    logout(request)
    # id=User.objects.get(id=request.user.id)
    # id.logout()
    return redirect("/")





from company_role.serializer import *
from  rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class UserList(generics.ListCreateAPIView):
    queryset = IntervieweeTestDetails.objects.filter(interviewer_id=1)
    serializer_class = InterviewwSerializer

    def get(self,request):
        queryset = IntervieweeTestDetails.objects.filter(interviewer_id__in=[1],started_at__isnull = False)
        data = []

        for i in queryset:

            data.append({
                "id":i.id,
                "interviewer_id":i.interviewer_id,
                "interviewer_name":i.interviewer.username,
                "Candidate_name":i.interviewee.name,
                "profile":i.interviewee.language,
                "Status":i.status,
                "cv":i.interviewee.cv.url,
                "level":i.interviewee.level,
                "date":i.started_at.strftime('%m-%d-%y')
            })


        return Response(data)
