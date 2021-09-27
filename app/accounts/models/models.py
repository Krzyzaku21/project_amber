from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.


class CreateUserManager(BaseUserManager):
    def _create_user(self, email, password, date_of_birth, is_admin, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, date_of_birth, is_admin=False, is_superuser=False, **extra_fields):
        return self._create_user(email, password, date_of_birth, is_admin, is_superuser, **extra_fields)

    def create_superuser(self, email, password, date_of_birth, is_admin=True, is_superuser=True, **extra_fields):
        return self._create_user(email, password, date_of_birth, is_admin, is_superuser, **extra_fields)


class CreateUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField()
    date_joined = models.DateTimeField(blank=False, default=timezone.now)
    username = models.CharField(max_length=191, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField(default='./images/accounts/user/default_user.png',
                               blank=True, upload_to='./images/accounts/user/')
    password = models.CharField(max_length=120, blank=False)
    password2 = models.CharField(max_length=120, blank=False)

    objects = CreateUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
