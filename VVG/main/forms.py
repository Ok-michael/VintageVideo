from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'required',
            'autofocus': 'autofocus'
        }),
        label='Username'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'required'
        }),
        label='Password'
    )
   
   
class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'User Name',
            'required': 'True',
            'autofocus': 'True'
        }),
        label='Username'
    )
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': 'True',
            'autofocus': 'True'
        }),
        label='FirstName'
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'True',
            'autofocus': 'True'
        }),
        label='LastName'
    )
    
    email = forms.CharField(
        max_length=200,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'True',
            'autofocus': 'True'
        }),
        label='Email'
    )
    
    password = forms.CharField(
        min_length=6,
        max_length=10,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'True',
            'autofocus': 'True'
        }),
        label='Password'
    )
    
    repeat_password = forms.CharField(
        min_length=6,
        max_length=10,
        widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Repeat password'
        })
    )

    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError('Username already in use!')
        return username
        
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError('Email already in use!')
        return email
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', 'Passwords did not match!')

        return cleaned_data
        