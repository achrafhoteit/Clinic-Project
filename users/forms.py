from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import NumberInput


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class AdminForm(forms.ModelForm):
    class Meta:
        model=models.Admin
        fields=['address','mobile','profile_pic']


class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','profile_pic']



class SecretaryUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class SecretaryForm(forms.ModelForm):
    class Meta:
        model= models.Secretary
        fields=['mobile', 'profile_pic']


class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name', 'username']

class PatientForm(forms.ModelForm):
    
    class Meta:
        model = models.Patient
        fields = ['address','mobile','symptoms']


class AppointmentForm(forms.ModelForm):
        
    class Meta:

        model=models.Appointment

        fields=['patient','doctor','start_time','end_time','description','fees_per_hour']

    
    patient =forms.ModelChoiceField(
        queryset=models.Patient.objects.all(),
        label = 'Select a Patient',
        empty_label="Patient Name and Notes"
    )

    doctor =forms.ModelChoiceField(
        queryset=models.Doctor.objects.all(),
        empty_label="Doctor Name and Department",
        label= 'Select a Doctor'
    )

    start_time = forms.DateTimeField(
        widget=NumberInput(attrs={'type': 'datetime-local'}))
    
    end_time = forms.DateTimeField(
        widget=NumberInput(attrs={'type': 'datetime-local'}))
    

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='Start Date',
        widget=NumberInput(attrs={'type': 'date'}))
    
    end_date = forms.DateField(
        label='End Date',
        widget=NumberInput(attrs={'type': 'date'}))