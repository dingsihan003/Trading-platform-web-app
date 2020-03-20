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

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True, label='email', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}),
                             max_length=100, error_messages={"required": "邮箱不能为空", "invalid": ""})

class ResetForm(forms.Form):
    email = forms.EmailField(required=True, label='email', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}),
                             max_length=100, error_messages={"required": "邮箱不能为空", "invalid": ""})
    newpwd = forms.CharField(required=True, label='newpassword', widget=forms.PasswordInput(
        attrs={"placeholder": "请输入新密码"}
    ))
    repwd = forms.CharField(required=True, label='新密码', widget=forms.PasswordInput(
        attrs={"placeholder": "请输入新密码"}))