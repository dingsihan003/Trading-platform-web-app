from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    location = forms.CharField(label='Location', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class emailForm(forms.Form):
    email=forms.CharField(max_length=100)

class locationForm(forms.Form):
    location=forms.CharField(max_length=100)