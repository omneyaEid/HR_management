from tabnanny import check
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# Create your models here.

class Attendance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    check_in=models.DateTimeField(blank=True, null=True)
    check_out=models.DateTimeField(blank=True, null=True)
    # created_at=models.DateTimeField(auto_now_add=True)
    
class ReviewAttendance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    check_in_late=models.BooleanField(default=False)
    check_out_early=models.BooleanField(default=False)
    day=models.DateField()
    # created_at=models.DateTimeField(auto_now_add=True)
@receiver(post_save, sender=User)
def createToken(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)
