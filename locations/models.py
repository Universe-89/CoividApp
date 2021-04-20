from django.db import models
from django.contrib.auth import get_user_model as user_model 
from phone_field import PhoneField

User = user_model()

# Create your models here.
class VisitedPlace(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="VisitedPlace",null=True)
    place = models.CharField(max_length=40, null=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.place)
