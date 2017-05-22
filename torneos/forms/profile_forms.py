from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

from ..models.profile_model import  Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        first_name = forms.CharField(required=True)
        last_name = forms.CharField(required=True)
        email = forms.EmailField(label='Your email', required=True)
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        bio = forms.CharField(widget=forms.Textarea)
        fields = ('bio',)

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )