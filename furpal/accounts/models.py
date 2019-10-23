from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


# class UserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, phone_number, birth_date, password=None, is_active=True, is_staff=False, is_admin=False, is_dogowner=False):
#         if not email:
#             raise ValueError("Users must have a valid email address")
#         if not password:
#             raise ValueError("Users must have a password")
#         user_obj = self.model(
#             email=self.normalize_email(email)
#         )
#         user_obj.set_password(password)
#         user_obj.first_name = first_name
#         user_obj.last_name = last_name
#         user_obj.phone_number = phone_number
#         user_obj.birth_date = birth_date
#         user_obj.staff = is_staff
#         user_obj.admin = is_admin
#         user_obj.active = is_active
#         user_obj.dogowner = is_dogowner
#         user_obj.save(using=self._db)
#         return user_obj

#     def create_staffuser(self, email, first_name, last_name, phone_number, birth_date, password=None):
#         user = self.create_user(email, first_name=first_name, last_name=last_name,
#                                 phone_number=phone_number, birth_date=birth_date, password=password, is_staff=True, is_dogowner=True)
#         return user

#     def create_superuser(self, email, first_name, last_name, phone_number, birth_date, password=None):
#         user = self.create_user(email, first_name=first_name, last_name=last_name,
#                                 phone_number=phone_number, birth_date=birth_date, password=password, is_staff=True, is_admin=True, is_dogowner=True)
#         return user

#     def create_dogowner(self, email, first_name, last_name, phone_number, birth_date, password=None):
#         user = self.create_user(email, first_name=first_name, last_name=last_name,
#                                 phone_number=phone_number, birth_date=birth_date, password=password, is_dogowner=True)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     phone_number = PhoneNumberField()
#     birth_date = models.DateField()
#     active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False)
#     admin = models.BooleanField(default=False)
#     dogowner = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     USERNAME_FIELD = 'email'

#     REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'birth_date']

#     objects = UserManager()

#     def __str__(self):
#         return self.email

#     def get_first_name(self):
#         return self.first_name

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_admin(self):
#         return self.admin

#     @property
#     def is_active(self):
#         return self.active

#     @property
#     def is_dogowner(self):
#         return self.dogowner

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have a valid email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj



class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# Should have the follow types: Admin, Staff, FurFriend, PetOwner
class UserType(models.Model):
    user_type = models.CharField(max_length=255)

    users = models.ManyToManyField(User, through='FurpalUser')

# join table between user and userType
class FurpalUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)

class FurFriend(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    birth_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

# named petowner in case expand to cats?
# every PetOwner must have a furfriend created first
class PetOwner(models.Model):
    owner_description = models.TextField(null=True)
    postal_code = models.CharField(max_length=20, null=True)

    fur_friend = models.OneToOneField("FurFriend", on_delete=models.PROTECT)

# Should have the following types: hourly, minute
class RateType(models.Model):
    type = models.CharField(max_length=255)
    
class Posts(models.Model):
    likes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    date_posted = models.DateField(auto_now=True)
    rate_type = models.ForeignKey(RateType, on_delete=models.CASCADE)
    rate_value = models.PositiveIntegerField()

    owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE)

class Pet(models.Model):
    name = models.TextField()
    breed = models.TextField()
    description = models.TextField(null=True)
    birth_date = models.DateField()

    owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE)
    post = models.OneToOneField(Posts, on_delete=models.CASCADE)

class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class PetImages(models.model):
#     image_path = models.FieldFIeld(upload_to='petimages/')

#     pet = models.ForeignKey(Pet)