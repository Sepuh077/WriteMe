from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(VerificationCode)
admin.site.register(Chat)
admin.site.register(Message)

