from django.forms import *
from ..models import CreateUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class RegisterUserForm(ModelForm):

    password = CharField(label="Password")
    password2 = CharField(label="Password repeat")

    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'password', 'password2', 'avatar']
        widgets = {
            'password': PasswordInput,
            'password2': PasswordInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class RegisterChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email',
                  'password', 'password2', 'avatar', 'is_active', 'is_admin']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            del self.fields['password2']

        def __init__(self, *args, **kwargs):
            super(RegisterChangeForm, self).__init__(*args, **kwargs)
            f = self.fields.get('user_permissions', None)
            if f is not None:
                f.queryset = f.queryset.select_related('content_type')

        def clean_password(self):
            return self.initial['password']
