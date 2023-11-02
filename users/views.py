from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone

import csv


def home_view(request):
    if request.user.is_authenticated:
        return redirect('after-login')
    return render(request,'users/index.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return redirect('after-login')
    return render(request,'users/adminclick.html')

def doctorclick_view(request):
    if request.user.is_authenticated:
        return redirect('after-login')
    return render(request,'users/doctorclick.html')


def secretaryclick_view(request):
    if request.user.is_authenticated:
        return redirect('after-login')
    return render(request,'users/secretaryclick.html')


def admin_signup_view(request):

    userForm = forms.AdminUserForm()
    adminForm = forms.AdminForm()

    mydict={'userForm':userForm, 'adminForm':adminForm}

    if request.method=='POST':

        userForm = forms.AdminUserForm(request.POST)
        adminForm=forms.AdminForm(request.POST,request.FILES)

        if userForm.is_valid() and adminForm.is_valid():

            user=userForm.save()
            user.set_password(user.password)
            user.save()

            admin = adminForm.save(commit=False)
            admin.user=user
            admin.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return redirect('admin-login')
    return render(request,'users/adminsignup.html', context=mydict)




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return redirect('doctor-login')
    return render(request,'users/doctorsignup.html',context=mydict)


def secretary_signup_view(request):
    userForm = forms.SecretaryUserForm()
    secretaryForm = forms.SecretaryForm()

    mydict={'userForm':userForm,'secretaryForm':secretaryForm}

    if request.method=='POST':

        userForm = forms.SecretaryUserForm(request.POST)
        secretaryForm = forms.SecretaryForm(request.POST, request.FILES)

        if userForm.is_valid() and secretaryForm.is_valid():

            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=secretaryForm.save(commit=False)
            doctor.user=user
            doctor.save()

            my_secretary_group = Group.objects.get_or_create(name='SECRETARY')
            my_secretary_group[0].user_set.add(user)
        return redirect('secretary-login')
    return render(request,'users/secretarysignup.html',context = mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_secretary(user):
    return user.groups.filter(name='SECRETARY').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('doctor-dashboard')
        # else:
        #     return render(request,'hospital/doctor/doctor_wait_for_approval.html')
    elif is_secretary(request.user):
        accountapproval = models.Secretary.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('secretary-dashboard')
        # else:
        #     return render(request,'hospital/secretary/secretary_wait_for_approval.html')
    elif request.user.is_superuser:
        return redirect('logout')





#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):

    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')

    #for three cards
    doctorcount=models.Doctor.objects.all().count()
    # pendingdoctorcount=models.Doctor.objects.all().count()

    patientcount=models.Patient.objects.all().count()
    # pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().count()
    # pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()


    #I can add secretaries also
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    }

    return render(request,'users/admin/dashboard.html',context=mydict)





# this view for sidebar click on admin page
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'users/admin/doctor.html')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all()
    return render(request,'users/admin/view_doctor.html',{'doctors':doctors})




@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save()
            return redirect('admin-view-doctor')
    return render(request,'users/admin/update_doctor.html',context=mydict)




@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return redirect('admin-view-doctor')
    return render(request,'users/admin/add_doctor.html',context=mydict)






#Same Thing for Secretary

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_secretary_view(request):
    return render(request,'users/admin/secretary.html')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_secretary_view(request):
    secretaries = models.Secretary.objects.all()
    return render(request,'users/admin/view_secretary.html',{'secretaries':secretaries})



@login_required(login_url='adminl-ogin')
@user_passes_test(is_admin)
def delete_secretary_from_hospital_view(request,pk):
    secretary = models.Secretary.objects.get(id=pk)
    user=models.User.objects.get(id=secretary.user_id)
    user.delete()
    secretary.delete()
    return redirect('admin-view-secretary')



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_secretary_view(request,pk):
    secretary=models.Secretary.objects.get(id=pk)
    user=models.User.objects.get(id=secretary.user_id)

    userForm = forms.SecretaryUserForm(instance=user)
    secretaryForm=forms.SecretaryForm(request.FILES,instance=secretary)
    mydict={'userForm':userForm,'secretaryForm':secretaryForm}

    if request.method=='POST':
        userForm=forms.SecretaryUserForm(request.POST,instance=user)
        secretaryForm=forms.SecretaryForm(request.POST,request.FILES,instance=secretary)

        if userForm.is_valid() and secretaryForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            secretary = secretaryForm.save()
            return redirect('admin-view-secretary')
    return render(request,'users/admin/update_secretary.html',context=mydict)




@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_secretary_view(request):

    userForm=forms.SecretaryUserForm()
    secretaryForm=forms.SecretaryForm()
    mydict={'userForm':userForm,'secretaryForm':secretaryForm}

    if request.method=='POST':
        userForm=forms.SecretaryUserForm(request.POST)
        secretaryForm=forms.SecretaryForm(request.POST, request.FILES)

        if userForm.is_valid() and secretaryForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            secretary = secretaryForm.save(commit=False)
            secretary.user=user
            secretary.save()

            my_secretary_group = Group.objects.get_or_create(name='SECRETARY')
            my_secretary_group[0].user_set.add(user)

        return redirect('admin-view-secretary')
    return render(request,'users/admin/add_secretary.html',context=mydict)





# Same thing For Patients

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'users/admin/patient.html')



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all()
    return render(request,'users/admin/view_patient.html',{'patients':patients})



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}

    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patientForm.save()
            return redirect('admin-view-patient')
    return render(request,'users/admin/update_patient.html',context=mydict)





@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return redirect('admin-view-patient')
    return render(request,'users/admin/add_patient.html',context=mydict)



#-----------------APPOINTMENT START--------------------------------------------------------------------

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'users/admin/appointment.html')



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):

    all_appointments = models.Appointment.objects.all()

    for app in all_appointments:
        if app.is_completed is False:
            current_time = timezone.now()
            print(current_time)
            if app.end_time <= current_time:
                app.is_completed = True
                app.save()

    if request.method == 'POST':

        form = forms.DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            print(start_date)

            end_date = form.cleaned_data['end_date']
            print(end_date)


            appointments=models.Appointment.objects.all().filter(
                start_time__range = (start_date, end_date),
                end_time__range = (start_date, end_date ))

    else:
        form = forms.DateRangeForm()
        appointments = []

    return render(request,'users/admin/view_appointment.html', {'form':form, 'appointments':appointments})




@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_appointment_from_hospital_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-view-appointment')



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_appointment_view(request,pk):

    appointment = models.Appointment.objects.get(id=pk)

    appointmentForm = forms.AppointmentForm(instance=appointment)

    mydict={'appointmentForm':appointmentForm}

    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST,instance=appointment)
        if appointmentForm.is_valid():
            appointmentForm.save()
            return redirect('admin-view-appointment')
    return render(request,'users/admin/update_appointment.html',context=mydict)



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):

    appointmentForm=forms.AppointmentForm()

    if request.method=='POST':

        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():

            appointmentForm.save()
        return redirect('admin-view-appointment')
    return render(request,'users/admin/add_appointment.html', {'appointmentForm':appointmentForm})



#--------------------- FOR GETTING BILL OF APPOINTMENT BY ADMIN START-------------------------


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_appointment_bill(request,pk):

    appointment = models.Appointment.objects.get(id=pk)

    duration = appointment.calculate_duration()

    patient = models.Patient.objects.get(id = appointment.patient_id)

    assignedDoctor = models.Doctor.objects.get(id=appointment.doctor_id)

    duration_in_minutes = duration.seconds / 60
    duration_in_hours = round(duration.seconds / 3600, 2)


    appointmentDict = {
        'appID' : pk,
        'patientName' : patient.user.first_name,
        'mobile' : patient.mobile,
        'address' : patient.address,
        'symptoms':patient.symptoms,
        'start_time' : appointment.start_time,
        'end_time' : appointment.end_time,
        'durationInMinutes' : duration_in_minutes,
        'durationInHours' : duration_in_hours,
        'assignedDoctor' : assignedDoctor.user.first_name,
        'fees_hour' : appointment.fees_per_hour,
        'totalFees' : appointment.calculate_total_fees()
    }

    return render(request,'users/admin/appointment_final_bill.html',context=appointmentDict)




#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view2(request,pk):
    
    appointment = models.Appointment.objects.get(id=pk)
    duration = appointment.calculate_duration()

    patient = models.Patient.objects.get(id = appointment.patient_id)

    assignedDoctor = models.Doctor.objects.get(id=appointment.doctor_id)

    duration_in_minutes = duration.seconds / 60
    duration_in_hours = round(duration.seconds / 3600, 2)

    appointmentDict = {
        'appID' : pk,
        'patientName' : patient.user.first_name,
        'mobile' : patient.mobile,
        'address' : patient.address,
        'symptoms':patient.symptoms,
        'start_time' : appointment.start_time,
        'end_time' : appointment.end_time,
        'durationInMinutes' : duration_in_minutes,
        'durationInHours' : duration_in_hours,
        'assignedDoctor' : assignedDoctor.user.first_name,
        'fees_hour' : appointment.fees_per_hour,
        'totalFees' : appointment.calculate_total_fees()
    }
    return render_to_pdf('users/download_bill2.html', appointmentDict)


def appointments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=appointments.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    appointments = models.Appointment.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Doctor', 'Patient', 'Start Time', 'End Time', 'Description', 'Fees Per Hour'])

    # Loop Thru and output
    for app in appointments:
        writer.writerow([f"{app.doctor.user.first_name} {app.doctor.user.last_name}", f"{app.patient.user.first_name} {app.patient.user.last_name}", app.start_time.strftime("%d/%m/%Y %I:%M %p"), app.end_time.strftime("%d/%m/%Y %I:%M %p"), app.description, app.fees_per_hour])

    return response    



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    
    all_appointments = models.Appointment.objects.all()

    for app in all_appointments:
        if app.is_completed is False:
            current_time = timezone.now()
            if app.end_time <= current_time:
                app.is_completed = True
                app.save()

    assigned_doctor = models.Doctor.objects.get(user_id = request.user.id)

    appointmentcount = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False).count()

    #for  table in doctor dashboard
    appointments = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False).order_by('-id')

    # patients_id=[]
    patients_unique_id =[]
    for a in appointments:
        # patients_id.append(a.patient_id)
        if a.patient_id not in patients_unique_id:
            patients_unique_id.append(a.patient_id)

    # patients=models.Patient.objects.all().filter(id__in = patients_id).order_by('-id')

    mydict={
    'patientcount':len(patients_unique_id),
    'appointmentcount':appointmentcount,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'users/doctor/dashboard.html',context=mydict)



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    return render(request,'users/doctor/patient.html', {'doctor':doctor})



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):

    assigned_doctor = models.Doctor.objects.get(user_id = request.user.id)

    appointments = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False)

    patients_unique_id =[]
    for a in appointments:
        if a.patient_id not in patients_unique_id:
            patients_unique_id.append(a.patient_id)

    patients=models.Patient.objects.all().filter(id__in = patients_unique_id).order_by('-id')

    # doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'users/doctor/view_patient.html', {'patients':patients})



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):

    # assigned_doctor = models.Doctor.objects.get(user_id = request.user.id)

    # appointments = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False)

    return render(request,'users/doctor/appointment.html')



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):

    all_appointments = models.Appointment.objects.all()

    for app in all_appointments:
        if app.is_completed is False:
            current_time = timezone.now()
            if app.end_time <= current_time:
                app.is_completed = True
                app.save()

    assigned_doctor = models.Doctor.objects.get(user_id = request.user.id)
    
    appointments = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False)

    return render(request,'users/doctor/view_appointment.html',{'appointments':appointments})



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):

    assigned_doctor = models.Doctor.objects.get(user_id = request.user.id)
    
    appointments = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False)

    return render(request,'users/doctor/delete_appointment.html',{'appointments':appointments})



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()

    return redirect('doctor-delete-appointment')

    # assigned_doctor = models.Doctor.objects.get(user_id = request.user.id)

    # appointments = models.Appointment.objects.all().filter(doctor_id=assigned_doctor.id, is_completed=False)

    # return render(request,'users/doctor/delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------





#---------------------------------------------------------------------------------
#------------------------ SECRETARY RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------


@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_dashboard_view(request):

    #for the table in admin dashboard
    patients=models.Patient.objects.all().order_by('-id')

    #for 2 cards
    patientcount=models.Patient.objects.all().count()

    appointmentcount=models.Appointment.objects.all().count()

    mydict={
    'patients':patients,
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    }

    return render(request,'users/secretary/dashboard.html',context=mydict)




@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_patient_view(request):
    return render(request,'users/secretary/patient.html')



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_view_patient_view(request):
    patients=models.Patient.objects.all().filter()
    return render(request,'users/secretary/view_patient.html',{'patients':patients})



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def delete_patient_from_hospital_view2(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('secretary-view-patient')



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def update_patient_view2(request,pk):

    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)

    mydict={'userForm':userForm,'patientForm':patientForm}

    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patientForm.save()
            return redirect('secretary-view-patient')
    return render(request,'users/secretary/update_patient.html',context=mydict)



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return redirect('secretary-view-patient')
    return render(request,'users/secretary/add_patient.html',context=mydict)



#-----------------APPOINTMENT START--------------------------------------------------------------------

@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_appointment_view(request):
    return render(request,'users/secretary/appointment.html')



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_view_appointment_view(request):
    appointments=models.Appointment.objects.all()

    for app in appointments:
        if app.is_completed is False:
            current_time = timezone.now()
            if app.end_time <= current_time:
                app.is_completed = True
                app.save()

    return render(request,'users/secretary/view_appointment.html',{'appointments':appointments})



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def delete_appointment_from_hospital_view2(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('secretary-view-appointment')



@login_required(login_url='admin-secretary')
@user_passes_test(is_secretary)
def update_appointment_view2(request,pk):

    appointment = models.Appointment.objects.get(id=pk)

    appointmentForm = forms.AppointmentForm(instance=appointment)

    mydict={'appointmentForm':appointmentForm}

    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST,instance=appointment)
        if appointmentForm.is_valid():
            appointmentForm.save()
            return redirect('secretary-view-appointment')
    return render(request,'users/secretary/update_appointment.html',context=mydict)




@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def secretary_add_appointment_view(request):

    appointmentForm=forms.AppointmentForm()

    if request.method=='POST':

        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():

            appointmentForm.save()
        return redirect('secretary-view-appointment')
    return render(request,'users/secretary/add_appointment.html', {'appointmentForm':appointmentForm})



@login_required(login_url='secretary-login')
@user_passes_test(is_secretary)
def admin_appointment_bill2(request,pk):

    appointment = models.Appointment.objects.get(id=pk)

    duration = appointment.calculate_duration()

    patient = models.Patient.objects.get(id = appointment.patient_id)

    assignedDoctor = models.Doctor.objects.get(id=appointment.doctor_id)

    duration_in_minutes = duration.seconds / 60
    duration_in_hours = round(duration.seconds / 3600, 2)


    appointmentDict = {
        'appID' : pk,
        'patientName' : patient.user.first_name,
        'mobile' : patient.mobile,
        'address' : patient.address,
        'symptoms':patient.symptoms,
        'start_time' : appointment.start_time,
        'end_time' : appointment.end_time,
        'durationInMinutes' : duration_in_minutes,
        'durationInHours' : duration_in_hours,
        'assignedDoctor' : assignedDoctor.user.first_name,
        'fees_hour' : appointment.fees_per_hour,
        'totalFees' : appointment.calculate_total_fees()
    }

    return render(request,'users/secretary/appointment_final_bill.html',context=appointmentDict)


#---------------------------------------------------------------------------------
#------------------------ SECRETARY RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
