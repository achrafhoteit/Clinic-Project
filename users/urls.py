from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name='home'),

    path('adminclick/', views.adminclick_view, name="admin-click"),
    path('doctorclick/', views.doctorclick_view, name="doctor-click"),
    path('secretaryclick/', views.secretaryclick_view, name="secretary-click"),

    path('adminsignup/', views.admin_signup_view, name="admin-signup"),
    path('doctorsignup/', views.doctor_signup_view, name='doctor-signup'),
    path('secretarysignup/', views.secretary_signup_view, name="secretary-signup"),

    path('adminlogin/', LoginView.as_view(template_name='users/adminlogin.html'), name='admin-login'),
    path('doctorlogin/', LoginView.as_view(template_name='users/doctorlogin.html'), name='doctor-login'),
    path('secretarylogin/', LoginView.as_view(template_name='users/secretarylogin.html'), name='secretary-login'),

    path('afterlogin/', views.afterlogin_view, name='after-login'),
    path('logout/', LogoutView.as_view(template_name='users/index.html'), name='logout'),


    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor/', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor/', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>/', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>/', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor/', views.admin_add_doctor_view,name='admin-add-doctor'),

    path('admin-secretary/', views.admin_secretary_view,name='admin-secretary'),
    path('admin-view-secretary/', views.admin_view_secretary_view,name='admin-view-secretary'),
    path('delete-secretary-from-hospital/<int:pk>/', views.delete_secretary_from_hospital_view,name='delete-secretary-from-hospital'),
    path('update-secretary/<int:pk>/', views.update_secretary_view,name='update-secretary'),
    path('admin-add-secretary/', views.admin_add_secretary_view,name='admin-add-secretary'),


    path('admin-patient/', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient/', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>/', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>/', views.update_patient_view,name='update-patient'),
    path('admin-add-patient/', views.admin_add_patient_view,name='admin-add-patient'),

    path('admin-appointment/', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment/', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('delete-appointment-from-hospital/<int:pk>/', views.delete_appointment_from_hospital_view,name='delete-appointment-from-hospital'),
    path('update-appointment/<int:pk>/', views.update_appointment_view,name='update-appointment'),
    path('admin-add-appointment/', views.admin_add_appointment_view,name='admin-add-appointment'),

    path('bill-appointment/<int:pk>/', views.admin_appointment_bill,name='appointment-bill'),
    path('download-pdf2/<int:pk>/', views.download_pdf_view2,name='download-pdf2'),

    path('appointments-csv/', views.appointments_csv, name='appointments-csv'),


]

#---------FOR DOCTOR RELATED URLS-------------------------------------
 
urlpatterns +=[
    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),

    path('doctor-patient/', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient/', views.doctor_view_patient_view,name='doctor-view-patient'),

    path('doctor-appointment/', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment/', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment/',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>/', views.delete_appointment_view,name='delete-appointment'),


]


#---------FOR SECRETARY RELATED URLS-------------------------------------

urlpatterns += [

    path('secretary-dashboard/', views.secretary_dashboard_view,name='secretary-dashboard'),

    path('secretary-patient/', views.secretary_patient_view,name='secretary-patient'),
    path('secretary-view-patient/', views.secretary_view_patient_view,name='secretary-view-patient'),
    path('delete-patient-from-hospital2/<int:pk>/', views.delete_patient_from_hospital_view2,name='delete-patient-from-hospital2'),
    path('update-patient2/<int:pk>/', views.update_patient_view2,name='update-patient2'),
    path('secretary-add-patient/', views.secretary_add_patient_view,name='secretary-add-patient'),

    path('secretary-appointment/', views.secretary_appointment_view,name='secretary-appointment'),
    path('secretary-view-appointment/', views.secretary_view_appointment_view,name='secretary-view-appointment'),
    path('secretary-add-appointment/', views.secretary_add_appointment_view,name='secretary-add-appointment'),

    path('delete-appointment-from-hospital2/<int:pk>/', views.delete_appointment_from_hospital_view2,name='delete-appointment-from-hospital2'),
    path('update-appointment2/<int:pk>/', views.update_appointment_view2,name='update-appointment2'),

    path('bill-appointment2/<int:pk>/', views.admin_appointment_bill2,name='appointment-bill2'),


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
