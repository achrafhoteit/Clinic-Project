from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import decimal



departments=[('Psychologist','Psychologist'),('Psychiatrist','Psychiatrist')]


# Create your models here.

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic= models.ImageField(default='default.jpg', upload_to='profile_pics')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    # get_name will act as an attribute not like a method
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    #get_id the same also
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return f'Admin {self.user.first_name}'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic= models.ImageField(default='default.jpg' ,upload_to='profile_pics')
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Psychologist')

    # get_name will act as an attribute not like a method
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    #get_id the same also
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)




class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    #Bshouf eza bshila aw bhot default None
    symptoms = models.CharField(max_length=100,null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
    

class Appointment(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    start_time=models.DateTimeField()
    end_time=models.DateTimeField()

    fees_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    description=models.TextField(max_length=500, blank=True)

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.patient.get_name} appointment with {self.doctor.get_name} on {self.start_time}'
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after the start time.")
        elif self.fees_per_hour <= 0:
            raise ValidationError("Fees must be a positive decimal value.")

        
    def calculate_duration(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return duration
        return None
    
    def calculate_total_fees(self):
        duration = self.calculate_duration()
        if (duration):
            hours, seconds = divmod(duration.seconds, 3600)
            duration_in_hours = duration.days * 24 + hours + seconds / 3600
            total_fees = decimal.Decimal(duration_in_hours) * self.fees_per_hour
            return round(total_fees, 2)
        else:
            return None


class Secretary(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(default='default.jpg', upload_to='profile_pics')
    mobile = models.CharField(max_length=20,null=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "Secretary " + self.user.first_name