from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import render

from .models import UserProfile


def confirm_registration(request):
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        user_profile = UserProfile.objects.get(confirmation_code=confirmation_code)
        user = user_profile.user
        user.is_active = True
        user_profile.save()
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('notices')
    return render(request, 'registration/confirm_registration.html')


