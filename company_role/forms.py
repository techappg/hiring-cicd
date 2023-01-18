from django import forms
from .models import Company_Profile
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class profileform(forms.ModelForm):
    class Meta:
        model = Company_Profile
        fields="__all__"






class Login_form(forms.Form):
     username = forms.CharField(max_length=10)
     password = forms.CharField(max_length=20,required=False)
