from django.db import models
from django.core.validators import DecimalValidator,MinValueValidator,MaxValueValidator
from django.contrib.auth import get_user_model as user_model
import  datetime 
from phone_field import PhoneField

User = user_model()

# Create your models here.
class BasicInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="basicinfo", null=True)
    date = models.DateField(default=datetime.date.today) 
    temp = models.DecimalField( max_digits = 4 ,decimal_places=1,validators=[DecimalValidator(max_digits = 4 ,decimal_places=1)])
    headache = models.BooleanField()
    running_nose = models.BooleanField()
    sore_throat = models.BooleanField()
    loss_smell_taste = models.BooleanField()
    difficulty_breathing = models.BooleanField()
    oxygen_level = models.IntegerField(validators=[MaxValueValidator(0,"To low value"),MaxValueValidator(100,"Might be incorrect")])
    travel = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.user)+str("-")+str(self.date)

class EmergencyContacts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="emergencycontacts",null=True)
    contact = models.EmailField()
    name = models.CharField(max_length=20, null=True)
    phone = PhoneField()
    objects = models.Manager()

    def __str__(self):
        return str(self.contact)

class HealthInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="healthinfo", null=True)
    diabetic = models.BooleanField()
    cancer_patient = models.BooleanField()
    cardiac_patient = models.BooleanField()
    asthama_patient = models.BooleanField()
    blood_pressure_patient = models.BooleanField()
    weak_immunity = models.BooleanField()
    other = models.TextField()
    objects = models.Manager()
    def __str__(self):
        return str(self.user)






