from django.forms import ModelForm
from django import forms
from LoginApp.models import User, Profile

from django.contrib.auth.forms import UserCreationForm

# Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','password1','password2')
        


