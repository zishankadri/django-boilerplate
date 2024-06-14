from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db.models import Q

from .utils import generate_ref_code
# from . import custom_fields

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not password:
            raise ValueError("A password was not provided while creating the user.")
         
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        # Add initial variables { 

        user.email_auth_token = generate_ref_code()
        # }
        user.save(using=self._db)

        return user

    def create_superuser(self , email, password):
        user = self.create_user(
            email = email,
            password = password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.verified_email = True
        user.save(using = self._db)
        return user
    
class UserAccount(AbstractBaseUser):
    CUSTOMER = 'CUSTOMER'
    CARRIER = 'CARRIER'

    USER_TYPE_CHOICES = (
        (CUSTOMER, "Customer"),
        (CARRIER, "Carrier"),
    )

    # Auth
    email = models.EmailField(max_length=254, unique=True)

    # Verification OTP
    verified_email = models.BooleanField(default=False)
    email_auth_token = models.CharField(max_length=12, blank=True)

    # DEFAULTS
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()
    
    class Meta:
        db_table = "useraccounts"

    @property
    def is_customer(self):
        return self.user_type == self.CUSTOMER

    @property
    def is_carrier(self):
        return self.user_type == self.CARRIER
    
    @property
    def is_verified(self):
        return (self.verified_email and self.verified_phone)

    def __str__(self):
        return str(self.email)
    
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




# class History(models.Model):
#     subject = models.CharField(max_length=255)
#     previous_value = models.CharField(max_length=255)
#     latest_value = models.CharField(max_length=255)
#     date = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.localtime)
#     user = models.ForeignKey("accounts.UserAccount", on_delete=models.CASCADE, related_name="history")

#     class Meta:
#         db_table = "history"


    # def record_history(self, subject, previous_value, latest_value):
    #     history = History(
    #         subject=subject,
    #         previous_value=str(previous_value),
    #         latest_value=str(latest_value),
    #         user=self
    #     )
    #     history.save()