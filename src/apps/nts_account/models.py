# python packages
import uuid
# django packages
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as UserManager_
from django.db import models


class UserManager(UserManager_):
    """ Custom UserManager for the custom user model

    """
    def _create_user(self, email, password, **extra_fields):
        """ Create and save a user with the given email and password.

        """
        if not email:
            raise ValueError('User must have a email address')
        if not password:
            raise ValueError('User must have a password')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create a user

        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create a super user

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    # Remove the first_name and last_name cols in the AbstractUser model
    first_name = None  # :type: ignore
    last_name = None  # :type: ignore

    # Username is really the user's "public id" field
    username = models.UUIDField(
        verbose_name='Public id',
        db_column='public_id',
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text='Public user identifier',
    )

    # First and last name do not cover name patterns around the globe
    name = models.CharField(
        verbose_name='User full name',
        blank=True,
        max_length=255,
    )

    # User's email address
    email = models.EmailField(
        verbose_name='Email address',
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        },
    )

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    def get_full_name(self):
        """Return the full name."""
        return self.name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name.split(' ')[0]

    def get_initials(self):
        """
        Return the initials of the user's name.
        Eg. Foo Bar Baz --> FB
        """
        name_words = self.name.split(' ')[:2]
        return ''.join(map(lambda x: x[0], name_words))

    def __str__(self):
        return self.name