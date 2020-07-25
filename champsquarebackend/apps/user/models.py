from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
# Create your models here.

class UserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        creates and saves a User with the given email and password
        """
        now = timezone.now()
        if not email:
            raise ValueError('You must provide email')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_staff=False, is_active=True, 
            is_superuser = False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """
        A user suitable for use in this project

        This is basically a copy of the core AbstractUser model but without a
        username field
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(
        _('First name'), max_length=255, blank=True)
    last_name = models.CharField(
        _('Last name'), max_length=255, blank=True)
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'),
                                       default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)