from django import forms
from ..models import CreateUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CreateUser
        fields = ['email', 'password', 'is_active']

    def clean_password(self):
        return self.initial["password"]
