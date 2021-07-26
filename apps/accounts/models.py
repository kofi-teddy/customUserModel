import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, phone, password=None):
        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            phone = phone,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, firstname, lastname, phone, password=None):
        user = self.create_user(
            email = email,
            password = password,
            firstname = firstname,
            lastname = lastname,
            phone = phone
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(max_length=200, default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(null=False, max_length=100, unique=True)
    firstname = models.CharField(null=False, max_length=100)
    lastname = models.CharField(null=False, max_length=100)
    phone = models.IntegerField(null=False, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phone']

    objects = UserManager()

    def __str__(self):
        return f"{str(self.email)} - {self.firstname}"

    def has_perm(self, perm, object = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



