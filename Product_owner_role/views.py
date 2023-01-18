# from django.shortcuts import render
from Product_owner_role.models import *
from django.shortcuts import render, redirect
from company_role.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
#
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url="/")
def update_profile(request):
        user = User.objects.get(id=request.user.id)
        if user.is_company == True:
           company_detail=True
           company_detail = Company_Profile.objects.get(id=user.company_id)
           request.session['update_password'] = company_detail.company_Password
        elif user.is_HR:
            hr_detail = Hr_Profile.objects.get(added_by_id=user.company_id,email=user.email)
            request.session['update_password'] = hr_detail.password

        elif user.is_superuser:
            user = User.objects.get(id=user.id)
            request.session['update_password'] =user.password


        if request.method=="POST":
            if user.is_company==True:
                company_detail = Company_Profile.objects.get(id=user.company_id)
                company_detail.company_Name = request.POST["username"]
                company_detail.company_email = request.POST["email"]
                company_detail.company_phone_no = request.POST["phone_number"]
                company_detail.company_address = request.POST["address"]
                company_detail.company_Password = request.POST["password"]
                company_detail.save()

            if user.is_HR==True:
                Hr=Hr_Profile.objects.get(added_by_id=user.company_id)
                Hr.name=request.POST["username"]
                Hr.email=request.POST["email"]
                Hr.phone_no=request.POST["phone_number"]
                Hr.password=request.POST["password"]
                Hr.save()

            user = User.objects.get(id=request.user.id)
            user.email=request.POST["email"]
            user.user_mobile=request.POST["phone_number"]
            user.password=request.POST["password"]
            user.set_password(user.password)
            user.save()
            updated=True
            print(user.username)
            print(user.password)
            u = authenticate(username=user.username, password=request.POST["password"])
            print(u,"this is u")
            if u is None:
              return  redirect("/")
            else:
                login(request,u)
                print("hello here")

        return render(request, "update_profile.html", locals())


            # return redirect("/dashboard_index")


            # return redirect("/da
        #
        # shboard_index")




