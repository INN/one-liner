from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from forms import RegisterForm, ServiceAddForm
from oneliner.models import Service, ServiceConfig


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
        org = request.user.userprofile.organization
        configured_services = ServiceConfig.objects.filter(organization=org)
        return render(request, 'profile.html', {'configured_services': configured_services})


@login_required
def survey(request):
    return render(request, 'survey.html')


@login_required
def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


@login_required
def service_add(request, service):
    service = Service.objects.get(name=service)

    if request.method == 'POST':
        form = ServiceAddForm(request.POST)
        if form.is_valid():
            org = request.user.userprofile.organization

            try:
                ServiceConfig.objects.get(organization=org, service=service)
                messages.error(request, "You already have a config stored for %s" % service.name)
            except ServiceConfig.DoesNotExist:
                config = ServiceConfig(
                    organization=org,
                    service=service,
                    account_id=form.data.get('account_id')
                )
                config.save()
                messages.success(request, "Configuration for %s saved" % service.name)
    else:
        form = ServiceAddForm()

    return render(request, 'service_add.html', {'service': service, 'form': form})
