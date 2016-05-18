from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class ServiceAddForm(forms.Form):
    account_id = forms.CharField(label='Account ID', max_length=100)
