from django import forms
import os.path
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from Uscholar.models import Profile, Student


class BootstrapInput(forms.TextInput):
    def __init__(self, placeholder, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapInput, self).__init__(attrs={
            'class': 'form-control input-sm',
            'placeholder': placeholder
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapInput, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class BootstrapSelect(forms.Select):
    def __init__(self, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapSelect, self).__init__(attrs={
            'class': 'form-control input-sm',
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapSelect, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label="Your Name")
    contact_email = forms.EmailField(required=True, label="Your Email")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Enter your phone number")
    contact_mobile = forms.CharField(required=False, validators=[phone_regex], max_length=17, label="Your Phone Number")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea, label="Your Message")


class OfflineResultForm(forms.Form):
    import_file = forms.FileField()


class ConfirmImportForm(forms.Form):
    import_file_name = forms.CharField(widget=forms.HiddenInput)
    original_file_name = forms.CharField(widget=forms.HiddenInput)

    def clean_import_file_name(self):
        data = self.cleaned_data['import_file_name']
        data = os.path.basename(data)
        return data


class EnterRollNumberForm(forms.Form):
    roll_number = forms.CharField(
        widget=BootstrapInput('Roll Number', size=6))
    via = forms.ChoiceField(
        choices=[('sms', 'SMS'), ('call', 'Call')],
        widget=BootstrapSelect(size=3))


class TokenForm(forms.Form):
    token = forms.CharField(
        widget=BootstrapInput('Enter OTP', size=6))

    def save(self):
        u_name = self.cleaned_data["username"]
        u_name = u_name.lower()
        pwd = self.cleaned_data["password"]
        email = self.cleaned_data['email']
        new_user = User.objects.create_user(u_name, email, pwd)

        new_user.first_name = self.cleaned_data["first_name"]
        new_user.last_name = self.cleaned_data["last_name"]
        new_user.save()

        cleaned_data = self.cleaned_data
        new_profile = Profile(user=new_user)
        new_profile.roll_number = cleaned_data["roll_number"]
        new_profile.phone_number = cleaned_data["phone_number"]
        new_profile.institute = cleaned_data["institute"]

        new_profile.save()

        return u_name, pwd

