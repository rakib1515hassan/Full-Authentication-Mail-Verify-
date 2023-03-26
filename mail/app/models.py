from django.db import models
from django.contrib.auth.models import User

# For Signal--------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

# For Email---------------------------------------------------
import uuid
from .utils import send_account_activation_email



# Create your models here.

class Profile(models.Model):
    gen = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    #objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Login Email Verification --------------------------------------
    email_token = models.CharField(max_length=200, default=0)
    is_email_verified = models.BooleanField(default=False)

    # Forget Password------------------------------------------------
    otp = models.IntegerField(default=0)


    pro_pic=models.ImageField(default='default_pic.jpg', upload_to="ProfilePic")
    gender=models.CharField(max_length=20, choices=gen, default='Male')
    date_of_birth=models.CharField(max_length=50, null=True, blank=True)
    phone=models.CharField(max_length=15, null=True, blank=True)
    blood=models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    # Siglar -----------------------------------------------------------------
    # def create_profile(sender, **kwargs):
    #     if kwargs['created']:
    #         user_profile = Profile.objects.create(user=kwargs['instance'])
    # post_save.connect(create_profile, sender=User)

    @receiver(post_save, sender=User)
    def send_email_token(sender, instance, created, **kwargs):
        try:
            if created:
                email_token = str(uuid.uuid4())
                pro_obj=Profile.objects.create(user = instance, email_token=email_token)
                pro_obj.save()
                email = instance.email
                send_account_activation_email(email, email_token)

        except Exception as e:
            print(e)

class Dicty(models.Model):
    name      = models.CharField(max_length=50)

class KeyVal(models.Model):
    container = models.ForeignKey(Dicty, db_index=True)
    key       = models.CharField(max_length=240, db_index=True)
    value     = models.CharField(max_length=240, db_index=True)