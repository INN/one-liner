from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User

from forms import RegisterForm


def home(request):
    return render_to_response('index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.data.get('username'))
                return HttpResponse("That username already exists!")
            except User.DoesNotExist:
                user = User(
                    username=form.data.get('username'),
                    password=form.data.get('password'),
                    email=form.data.get('email')
                )
                user.save()
                return HttpResponse("Thanks for registering!")
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
