from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django_registration.forms import RegistrationForm

import random
import string

from boardproj.settings import DEFAULT_FROM_EMAIL
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            authors_group = Group.objects.get(name='authors')
            user.groups.add(authors_group)

            confirmation_code = generate_confirmation_code()
            profile = UserProfile(user=user, confirmation_code=confirmation_code)
            profile.save()

            send_confirmation_email(user.email, confirmation_code)

            return redirect('confirm')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def generate_confirmation_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(10))
    return code


def send_confirmation_email(email, confirmation_code):
    subject = 'Register confirm'
    message = (f'Your confirmation code: {confirmation_code}')
    from_email = DEFAULT_FROM_EMAIL
    to_email = [email]
    send_mail(subject, message, from_email, to_email)
