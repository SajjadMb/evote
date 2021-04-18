from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class ElectionUserManager(BaseUserManager):
    def create_user(self, email, full_name, profile_photo, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            profile_photo=profile_photo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, profile_photo, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            profile_photo = profile_photo,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class ElectionUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(blank=True, max_length=255)
    job = models.CharField(blank=True, max_length=255)
    profile_photo = models.ImageField(upload_to='EVOTE/media/pic_folder/election_user', default='/root/Desktop/EVOTE/media/pic_folder/None/anonymous.jpg', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ElectionUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','profile_photo']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        return self.full_name

    def get_job(self):
        return self.job

    def get_photo(self):
        return self.profile_photo
