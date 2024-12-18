from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    sur_name = models.CharField(max_length=255)
    for_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "sur_name", "for_name"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def get_age(self):
        today = timezone.now()
        age = today.year - self.birth.year
        if (today.month, today.day) < (self.birth.month, self.birth.day):
            age -= 1
        return age

class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.phone_number} - {self.code} - {self.created}"