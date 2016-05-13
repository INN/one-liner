from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from forms import RegisterForm


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/profile/')
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
                return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    # TODO: This doesn't work for identifying first login:
    if request.user.last_login is None:
        return HttpResponseRedirect('/accounts/survey/')
    else:
        return render(request, 'profile.html')


@login_required
def survey(request):
    return render(request, 'survey.html')
