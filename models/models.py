from django.db import models


from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """
    Default user class, just in case we want to add something extra in the future.
    """
    pass

