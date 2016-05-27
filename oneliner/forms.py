from django import forms
from .models import PAGEVIEWS_CHOICES, SIZE_CHOICES, BUDGET_CHOICES


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), label='Password')


class ServiceForm(forms.Form):
    account_id = forms.CharField(label='Account ID', max_length=100)


class OrgSurvey(forms.Form):
    name = forms.CharField(
        label="What's your company's name?", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'My Company Name'})
    )
    url = forms.URLField(
        label='And URL?',
        widget=forms.URLInput(attrs={'placeholder': 'http://mycompany.com'})
    )
    size = forms.ChoiceField(
        label='How big is your team?',
        widget=forms.RadioSelect, choices=SIZE_CHOICES
    )
    budget = forms.ChoiceField(
        label='What is your monthly budget for analytics services?',
        widget=forms.RadioSelect, choices=BUDGET_CHOICES
    )
    pageviews = forms.ChoiceField(
        label='About how many page views do you serve per month?',
        widget=forms.RadioSelect, choices=PAGEVIEWS_CHOICES
    )
