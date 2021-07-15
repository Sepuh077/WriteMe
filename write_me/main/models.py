from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='./logo/default.png', upload_to='./Profile')
    birth_date = models.DateField(default=datetime.date(2001, 1, 1))
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f'Username: {self.user.username}, Name: {self.user.first_name}, Last name: {self.user.last_name}'


class Chat(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='first_user')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='second_user')

    def __str__(self):
        return f'Chat with {self.user1.user.username} and {self.user2.user.username}'


class Message(models.Model):
    replied_from_id = models.IntegerField(null=True, default=None)
    replied_text = models.TextField(blank=True, null=True, default=None)
    chat = models.ForeignKey(Chat, models.CASCADE)
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(default=datetime.datetime.now, blank=False)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Message: {self.message}'


class VerificationCode(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'For {self.profile.user.username} verification code is {self.code}'
