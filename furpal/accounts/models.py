from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, birth_date, password=None, is_active=True, is_staff=False, is_admin=False, is_dogowner=False):
        if not email:
            raise ValueError("Users must have a valid email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.phone_number = phone_number
        user_obj.birth_date = birth_date
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.dogowner = is_dogowner
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, phone_number, birth_date, password=None):
        user = self.create_user(email, first_name=first_name, last_name=last_name,
                                phone_number=phone_number, birth_date=birth_date, password=password, is_staff=True, is_dogowner=True)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, birth_date, password=None):
        user = self.create_user(email, first_name=first_name, last_name=last_name,
                                phone_number=phone_number, birth_date=birth_date, password=password, is_staff=True, is_admin=True, is_dogowner=True)
        return user

    def create_dogowner(self, email, first_name, last_name, phone_number, birth_date, password=None):
        user = self.create_user(email, first_name=first_name, last_name=last_name,
                                phone_number=phone_number, birth_date=birth_date, password=password, is_dogowner=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    birth_date = models.DateField()
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    dogowner = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'birth_date']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def is_dogowner(self):
        return self.dogowner
