from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from forms import RegisterForm, ServiceForm, OrgSurvey
from oneliner.models import Service, ServiceConfig, Organization


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


def one_liner_js(request, account_id):
    org = Organization.objects.get(id=account_id)
    services = [
        service.to_json() for service in
        ServiceConfig.objects.filter(organization=org)
    ]
    return render(
        request, 'one_liner_js.html', {'account_id': account_id, 'services': services},
        content_type='application/javascript'
    )


def instructions(request):
    return render(request, 'instructions.html')


@login_required
def profile(request):
    if request.user.userprofile.organization is None:
        return HttpResponseRedirect('/accounts/survey/')
    else:
        org = request.user.userprofile.organization
        configured_services = ServiceConfig.objects.filter(organization=org)
        return render(request, 'profile.html', {
            'configured_services': configured_services,
            # TODO: the domain in this url should be dynamic
            'one_liner_src': 'http://localhost:8000/js/%s/app.js' % org.id
        })


@login_required
def survey(request):
    if request.method == 'POST':
        form = OrgSurvey(request.POST)
        if form.is_valid():
            try:
                Organization.objects.get(name=form.data.get('name'), url=form.data.get('url'))
                messages.error(request, "A Company with that name and URL already exists")
            except Organization.DoesNotExist:
                org = Organization(
                    name=form.data.get('name'),
                    url=form.data.get('url'),
                    budget=form.data.get('budget'),
                    pageviews=form.data.get('pageviews'),
                    size=form.data.get('size')
                )
                org.save()
                messages.success(
                    request, "Company details saved. You are ready to start using One Liner!")
                return HttpResponseRedirect('/accounts/profile/')
    else:
        form = OrgSurvey()

    return render(request, 'survey.html', {'form': form})


@login_required
def services(request):
    services = Service.objects.all()
    org = request.user.userprofile.organization
    existing_configs = []

    for config in ServiceConfig.objects.filter(organization=org):
        existing_configs.append(config.service.id)

    return render(
        request, 'services.html', {'services': services, 'existing_configs': existing_configs})


@login_required
def service_add(request, service):
    service = Service.objects.get(name=service)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
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
                return HttpResponseRedirect('/accounts/profile/')
    else:
        form = ServiceForm()

    return render(request, 'service_add.html', {'service': service, 'form': form})


@login_required
def service_edit(request, service):
    service = Service.objects.get(name=service)
    org = request.user.userprofile.organization
    existing = ServiceConfig.objects.get(organization=org, service=service)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            existing.account_id = form.data.get('account_id')
            existing.save()
            messages.success(request, "Configuration for %s updated" % service.name)
    else:
        form = ServiceForm({'account_id': existing.account_id})

    return render(request, 'service_edit.html', {'service': service, 'form': form})


@login_required
def service_remove(request, service):
    service = Service.objects.get(name=service)
    org = request.user.userprofile.organization
    try:
        existing = ServiceConfig.objects.get(organization=org, service=service)
        existing.delete()
        messages.success(request, "Successfully removed %s from your configuration" % service.name)
    except ServiceConfig.DoesNotExist:
        messages.error(request, "There is no saved configuration for that service.")

    return HttpResponseRedirect('/')
