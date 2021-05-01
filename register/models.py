from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField

class MyAccountManager(BaseUserManager):
    def create_user(self,email, name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not phone:
            raise ValueError("Users must have a phone number")
        if not name:
            raise ValueError("Users must have a name")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone = phone
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,email, name, phone, password):
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            phone = phone
        )
        user.is_admin=True
        user.is_staff = True
        user.is_superuser = True
        user.is_active=True
        user.set_password(password)
        user.save(using = self._db)
        return user


class Account(AbstractBaseUser):
    email          = models.EmailField(primary_key=True)
    date_joined    = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login     = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin       = models.BooleanField(default=False)
    is_staff       = models.BooleanField(default=False)
    is_superuser   = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=False)
    phone          = PhoneField(help_text='Phone number')
    name           = models.CharField(max_length=30)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name','phone']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True