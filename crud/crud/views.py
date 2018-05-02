from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from social_django.views import disconnect

AUTH_BACKEND = 'google-oauth2'


@login_required
def logout(request):
    django_logout(request)
    disconnect(request, AUTH_BACKEND)
    return render(request, 'registration/login.html')
