from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            return TypeError("User should have username")
        if email is None:
            return TypeError("User should have email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            return TypeError("Password should not be empty!")
        user = self.create_user(username, email, password)

        user.is_staff = True
        user.is_owner = True
        user.is_active = True
        user.is_superuser = True

        user.parent = user
        user.created_by = user
        user.updated_by = user

        user.save()
        return user

    def create_vendor(self, username, email, password):
        if password is None:
            return TypeError("Password should not be empty!")

        user = self.create_user(username, email, password)

        user.is_staff = True
        user.is_vendor = True
        user.is_active = True
        user.save()

        return user


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    # TODO: phone number field need to add

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True, blank=True, related_name='creator')
    updated_by = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True, blank=True, related_name='updater')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
