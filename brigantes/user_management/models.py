from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.forms.models import model_to_dict
from django.db.models.fields.files import ImageFieldFile

# Create your models here.
class UserProfileManager(BaseUserManager):
    """ Helps work with custom user manager."""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a user object."""

        if not email:
            raise ValueError('User must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """ Create super user."""

        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ User profile model."""
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='users/photos', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    

    def as_dict(self, fields=None):
        if not fields:
            fields = [
                'last_login', 'is_superuser', 'email', 'first_name', 'last_name', 'photo', 'is_active', 'is_staff' 'date_joined']
            
        obj_dict = model_to_dict(self, fields=fields)

        for k, v in obj_dict.items():
            if isinstance(v, datetime):
                obj_dict[k] = str(v)
            if isinstance(v, ImageFieldFile):
                if v:
                    obj_dict[k] = v.url
                else:
                    obj_dict[k] = ''
        
        return obj_dict
