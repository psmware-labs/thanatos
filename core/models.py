from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, \
    PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # return the newly created user
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # assign Usermanager to the objects mixin
    objects = UserManager()
    # set email as default username field
    USERNAME_FIELD = 'email'


class Account(models.Model):
    """Accounts to be used for a group of questions"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class PrimaryMetric(models.Model):
    """Primary Metrics to be used for a group of questions"""
    metric = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.metric


class SecondaryMetric(models.Model):
    """Secondary Metrics to be used for a group of questions"""
    metric = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.metric


class TertiaryMetric(models.Model):
    """Tertiary Metrics to be used for a group of questions"""
    metric = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.metric


class Question(models.Model):
    """Questions to be used for Theta scoring"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    primary_metric = models.ForeignKey('PrimaryMetric',
                                       on_delete=models.PROTECT)
    secondary_metric = models.ForeignKey('SecondaryMetric',
                                         on_delete=models.PROTECT)
    tertiary_metric = models.ForeignKey('TertiaryMetric',
                                        on_delete=models.PROTECT)

    def __str__(self):
        return self.primary_metric.metric + \
            self.secondary_metric.metric + \
            self.tertiary_metric.metric
