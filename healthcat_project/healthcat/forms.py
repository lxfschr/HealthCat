from django import forms
from django.contrib.auth.models import User
from models import *

class ProfileForm(forms.ModelForm):
    username = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Email Address...'}))
    password2 = forms.CharField(max_length = 200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Confirm Password...'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Password...'}))
    class Meta:
        model = Person
        exclude = ('user',)
        widgets = {
                   'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number...'}),
                   'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code...'}),
                   'picture': forms.FileInput(),
                  }

class RegistrationForm(forms.Form):
    username = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Email Address...'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Password...'}))
    password2 = forms.CharField(max_length = 200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Confirm Password...'}))
    first_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'First Name...'}))
    last_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Last Name...'}))
    phone_number = forms.CharField(max_length = 13, 
                                label='Phone Number', 
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Phone Number...'}))
    zip_code = forms.CharField(max_length = 5, 
                                label='Zip Code', 
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Zip Code...'}))
    class Meta:
        model = User
        fields = ("first_name","last_name", "username", "password1", "password2")
    
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Email Address...'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(username__exact=email):
            raise forms.ValidationError("Sorry, we do not have an accout with that email.")
        return email