from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core import mail
from write_me.settings import EMAIL_HOST_USER, MEDIA_URL
from django.template.loader import render_to_string
import re
# from socket import A
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
import random
from .forms import *
from .models import *


def is_user_matches(search_text, text_len, user):
    if search_text[0] == '@':
        if len(user.username) < text_len - 1:
            if search_text[1:len(user.username) + 1].lower() == user.username.lower():
                return True
        else:
            if search_text[1:].lower() == user.username[:text_len - 1].lower():
                return True
    else:
        name = (user.first_name + " " + user.last_name).lower()
        if len(name) < text_len:
            if search_text[:len(name)].lower() == name or search_text.lower() == (user.last_name + " " +
                                                                                  user.first_name).lower():
                return True
        else:
            if search_text == name[:text_len] or search_text.lower() == (user.last_name + " " +
                                                                         user.first_name)[:text_len].lower():
                print(search_text)
                print(name[:text_len])
                return True

    return False


def send_email(to, subject, html_file, context, files):
    html_content = render_to_string(html_file, context)
    message = mail.EmailMessage(
        subject,
        html_content,
        EMAIL_HOST_USER,
        to,
    )
    for file in files:
        message.attach(file.name, file.read(), file.content_type)
    message.content_subtype = 'html'
    message.send(fail_silently=False)


# Create your views here.
@login_required(login_url='login')
def main(request):
    if request.user.is_superuser:
        return redirect('login')

    if request.method == "GET":
        print(request.GET.get('search'))
        search_text = request.GET.get('search')
        if search_text:
            return redirect(f'search/?search={search_text.replace(" ", "+")}', search_text=search_text)
    form = None
    context = {
        'user': Profile.objects.get(user=request.user),
        'profiles': Profile.objects.all(),
        'form': form,
        'media': MEDIA_URL,
    }
    return render(request, 'templates/index.html', context)


@login_required(login_url='login')
def search(request, search_text=None):
    if request.user.is_superuser:
        return redirect('login')
    if request.method == "GET":
        search_text = request.GET.get('search')

    matching_profiles = []
    if search_text:
        search_text = str(re.sub(' +', ' ', search_text)).lstrip().rstrip()
        print(search_text)
        profiles = Profile.objects.all()
        text_len = len(search_text)
        for profile in profiles:
            if is_user_matches(search_text, text_len, profile.user):
                matching_profiles.append(profile)

    context = {
        'profiles': matching_profiles,
        'user': Profile.objects.get(user=request.user),
        'media': MEDIA_URL,
    }
    return render(request, 'templates/search.html', context)


@login_required(login_url='login')
def chat(request, profile_id):
    try:
        my_profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(id=profile_id)
        chats = Chat.objects.filter(user1=my_profile, user2=other_profile) \
            | Chat.objects.filter(user2=my_profile, user1=other_profile)
        if request.method == "POST":
            message = request.POST.get('message')
            if message != '' and not message.isspace():
                if not chats:
                    chats = [Chat.objects.create(user1=my_profile, user2=other_profile)]

                Message.objects.create(
                    chat=chats[0],
                    from_user=my_profile,
                    message=message,
                )

        messages = [] if not chats else Message.objects.filter(chat=chats[0]).order_by('sent_date')
        context = {
            'my_profile': my_profile,
            'other_profile': other_profile,
            'all_chats': Chat.objects.filter(user1=my_profile) | Chat.objects.filter(user2=my_profile),
            'messages': messages,
            'media': MEDIA_URL,
        }
        return render(request, 'templates/chat.html', context)
    except Exception as exc:
        print(exc)
        return redirect('home')


def sign_in(request):
    logout(request)
    if request.method == "POST":
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=username_or_email, password=password)
        if user is None:
            user = authenticate(username=username_or_email, password=password)

        if user is not None and (user.is_superuser or Profile.objects.get(user=user).is_registered):
            login(request, user)
            return redirect('home')

    return render(request, 'templates/sign_in.html', {'media': MEDIA_URL})


def sign_up(request):
    logout(request)
    form = Registration()
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            code = random.randint(100000, 999999)
            send_email([request.POST.get('email')], 'Verification', 'templates/html_message.html', {'code': code}, [])
            user = form.save()
            profile = Profile.objects.create(user=user)
            VerificationCode.objects.create(profile=profile, code=code)
            return redirect('verify', profile_id=profile.id)

    context = {
        'form': form,
        'media': MEDIA_URL,
    }
    return render(request, 'templates/sign_up.html', context)


def verify(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)
        verification = VerificationCode.objects.get(profile=profile)
        print(verification)
        if request.method == "POST":
            code = request.POST.get('code')
            if code == verification.code:
                profile.is_registered = True
                profile.save()
                verification.delete()
                return redirect('login')

        return render(request, 'templates/verify.html')
    except Exception as exc:
        print(exc)
        return redirect('sign_up')
