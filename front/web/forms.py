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
    email=forms.EmailField(max_length=100)

class locationForm(forms.Form):
    location=forms.CharField(max_length=100)

class ListingForm(forms.Form):
    product_title = forms.CharField(label='product_title', max_length=100)
    product_base_price = forms.FloatField(label='product_base_price')
    product_description = forms.CharField(label='product_description', max_length=500)
    sold = forms.BooleanField(required=False)