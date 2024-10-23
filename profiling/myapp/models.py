from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, fullname, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, fullname, password=None):
        user = self.create_user(email, username, fullname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin