from django import forms
from django.contrib.auth.models import User
from models import *

# making http requests and json
import urllib2,urllib,httplib,json



class IconName(object):
    def get_icon_name(self):
        return self._icon_name
    def set_icon_name(self, value):
        self._icon_name = value
    icon_name = property(get_icon_name, set_icon_name)

class CharFieldWithIcon(forms.CharField, IconName):
    pass

class Tooltip(object):
    def get_tooltip(self):
        return self._tooltip
    def set_tooltip(self, value):
        self._tooltip = value
    tooltip = property(get_tooltip, set_tooltip)

class CharFieldWithIconAndTooltip(forms.CharField, IconName, Tooltip):
    pass

class BowlForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        error_css_class = 'error'
        required_css_class = 'required'

        model = Bowl
        exclude = ('owner','serial_number', 'pets')
        widgets = {
                   'name': forms.TextInput(attrs={'label':'Name', 
                                          'autofocus': 'autofocus', 
                                          'class':'width-200 form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                          'placeholder':'eg: Cat Bowl'}),
                   'ip_address': forms.TextInput(attrs={'label':'IP Address', 'autofocus': 'autofocus', 'class':'width-200 form-control' + ' ' + error_css_class + ' ' + required_css_class, 'placeholder':'eg: 128.1.109.20'}),
                  }
        labels = {
            "name": "Bowl Name",
            "ip_address": "Bowl IP Address",
        }
        
    def clean(self):
        cleaned_data = super(BowlForm,self).clean()
        return cleaned_data

    '''def clean_ip_address(self):
        print "in clean_ip_address"
        ip_address = self.cleaned_data.get('ip_address')
        try:
            r = urllib2.urlopen(ip_address+'connect').read()
            print r
        except:
            raise forms.ValidationError("Could not connect.")
        
        return ip_address'''


class RegistrationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    username = forms.EmailField(max_length = 40, 
                                label='Email', 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: alex@healthcat.com',
                                           'autofocus': 'autofocus'})
                                )
    password1 = forms.CharField(max_length = 16, 
                                label='Password', 
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: 1234'})
                                )
    password2 = forms.CharField(max_length = 16,
                                label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: 1234'})
                                )
    first_name = forms.CharField(max_length = 20, 
                                 label='First Name',
                                 widget=forms.TextInput(
                                    attrs={'class':'form-control' + ' ' + required_css_class, 
                                           'placeholder':'eg: Alex'})
                                )
    last_name = forms.CharField(required=False, 
                                label='Last Name',
                                max_length = 20, 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control', 
                                           'placeholder':'eg: Fischer'})
                                )
    zip_code = CharFieldWithIconAndTooltip(required=False, max_length = 5, 
                                label='Zip Code', 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class, 
                                           'placeholder':'eg: 15213'})
                                )
    photo = forms.ImageField(required=False,
                                  label='Photo',
                                 )
    class Meta:
        error_css_class = 'error'
        required_css_class = 'required'

        model = User
        fields = ("first_name","last_name", "username", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['zip_code'].icon_name = 'glyphicon glyphicon-question-sign'
        self.fields['zip_code'].tooltip = 'To compare your pets to other pets in your area.'

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
    error_css_class = 'error'
    required_css_class = 'required'

    email = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Email Address...'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(username__exact=email):
            raise forms.ValidationError("Sorry, we do not have an accout with that email.")
        return email

class ChangePasswordForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    error_css_class = 'error'
    required_css_class = 'required'

    password1 = forms.CharField(max_length = 16, 
                                label='New Password', 
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: 1234'}))
    password2 = forms.CharField(max_length = 16,
                                label='Confirm New Password',
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: 1234'}))
    def clean(self):
        cleaned_data = super(ChangePasswordForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class PetForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        error_css_class = 'error'
        required_css_class = 'required'

        model = Pet
        exclude = ('owner',)
        widgets = {
                   'name': forms.TextInput(attrs={'label':'Name', 'autofocus': 'autofocus', 'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 'placeholder':'eg: Mr. Bigglesworth'}),
                   'rfid': forms.TextInput(attrs={'label':'RFID #', 'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 'placeholder':'eg: C02002F18538AE2DFDC1C35'}),
                   'photo': forms.FileInput()
                  }
        labels = {
            "name": "Pet Name",
            "rfid": "RFID #",
            "photo": "Pet Photo"
        }
        
    def clean(self):
        cleaned_data = super(PetForm,self).clean()
        return cleaned_data

class FeedingIntervalForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    class Meta:
        error_css_class = 'error'
        required_css_class = 'required'

        model = FeedingInterval
        exclude = ('pet',)
        widgets = {
                   'start': forms.TimeInput(attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 'placeholder':'eg: 12:00 am'}),
                   'end': forms.TimeInput(attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 'placeholder':'eg: 11:59 pm'}),
                   'amount': forms.NumberInput(attrs={'autofocus': 'autofocus', 'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 'placeholder':'eg: 10'}),
                  }
        labels = {
            "amount": "Amount (grams)",
            "start": "Start Time",
            "end": "End Time"
        }

    def clean(self):
        cleaned_data = super(FeedingIntervalForm,self).clean()
        return cleaned_data