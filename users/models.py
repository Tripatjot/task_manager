from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Users(AbstractBaseUser):
    name            = models.CharField(max_length=25, null=False, blank=False, default=True)
    email           = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    password        = models.CharField(max_length=1024, null=True, blank=True)
    registered_on   = models.DateTimeField(auto_now_add=True)
    STATUS = [
        (0,"manager"),
        (1,"emplyoee")
    ]
    user_role       = models.IntegerField(choices=STATUS, default=1)
    current_status  = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'

    def _str_(self):
        return self.email
