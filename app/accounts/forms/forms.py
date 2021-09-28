from django import forms
from ..models import CreateUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class RegisterUserForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password repeat", widget=forms.PasswordInput)

    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'password', 'password2', 'avatar']

    def clean_password2(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password is not None and password != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CreateUser
        fields = ['email', 'password', 'is_active']

    def clean_password(self):
        return self.initial["password"]
