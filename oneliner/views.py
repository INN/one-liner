from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from forms import RegisterForm


def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.data.get('username'))
                messages.error(request, "That username is already taken!")
            except User.DoesNotExist:
                User.objects.create_user(
                    form.data.get('username'),
                    email=form.data.get('email'),
                    password=form.data.get('password')
                )
                messages.success(request, "Thanks for registering!")
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')
