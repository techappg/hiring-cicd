"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Interviewee_role.views import *
from Product_owner_role.views import *
from company_role.views import *
from Sample_Paper.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register', company_Register,name='company_Register'),
    path('company_register', companyRegister,name='company_Register'),
    path('dashboard_index', dashboard_index,name='dashboard_index'),
    path('', Admin_login,name='Admin_login'),
    # path('add_language', create_language,name='create_language'),
    path('get_language', get_language,name='get_language'),
    # path('add_level', create_level,name='create_level'),
    path('get_level', get_level,name='get_level'),
    path('get_allcompanies', get_allcompanies,name='create_level'),
    path('add_questions', add_questions,name='add_questions'),
    path('create_sample_paper', create_sample_paper,name='create_sample_paper'),
    path('add_interviwee',interviwee_register,name='interviwee'),
    path('add_hr',Hr_profile,name='add_hr'),
    path('add',new_value,name='add_hr'),
    path('display_sample_paper',get_sample,name='add_hr'),
    path('view/<str:public_url>',view_sample_paper,name='add_hr'),
    path('add_duration',add_duration,name='add_hr'),
    path('company/<str:id>',view_particular_company_details,name='add_hr'),

    path('dummy',dummy,name='dummy'),
    path('link/<str:id>',link_detail,name='link'),
    path('get_paper',get_paper,name='link'),
    path('all_hr',all_hr_record,name='all_hr'),
    path('all_record_interviwee/<str:type>',interviwee_task_details,name='link'),
    path('deactivate/<str:id>',decativate_company,name='deactivate'),
    path('activate/<str:id>',activate_company,name='deactivate'),
    path('update',update_profile,name='up'),
    path('company_update/<str:id>',update_particular_company_details,name='update'),
    path('hr/<str:id>',view_particular_hr_detail,name='update'),
    path('update_hr_details/<str:id>',update_particular_hr_details,name='update'),
    path('interviwee/<int:id>',particular_interviweee_detail,name='update'),
    path('pie-chart/', pie_chart, name='pie-chart'),
    path('all_sample', all_Samplepaper, name='all'),
    path('all_sample_paper/<str:id>', particular_sample_paper_details, name='sample'),
    path('get_sample_paper_details/<str:id>', get_sample_paper_details, name='sample1'),
    path('view_company/<str:type>', view_company, name="view_company"),
    path('detail_company/<str:id>', detail_company, name="view_company"),
    path("submitanswer",submit_answer,name="testing"),
    path("upload_file",upload_file,name="upload"),
    path("otp",otp_verify,name="otp_verify"),
    path("check",UserList.as_view(),name="check"),
    path("profile_logout",profile_logout,name="logout"),
    path("password_forgot",password_reset,name="password_forget"),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         reset, name='reset'),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
