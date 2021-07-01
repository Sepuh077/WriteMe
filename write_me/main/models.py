from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='./logo/default.png', upload_to='./Profile')
    birth_date = models.DateField(default=datetime.date(2001, 1, 1))
    is_registered = models.BooleanField(default=False)


class Chat(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='first_user')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='second_user')


class Message(models.Model):
    chat = models.ForeignKey(Chat, models.CASCADE)
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sent_time = models.DateTimeField(default=now())
    message = models.CharField(max_length=1000)


class VerificationCode(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
