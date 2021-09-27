from rest_framework import serializers
from accounts.models import CreateUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password', 'password2', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        createuser = CreateUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        createuser.set_password(password)
        createuser.save()
        return createuser

    def __init__(self, *args, **extra_kwargs):
        super().__init__(*args, **extra_kwargs)
        del self.fields['password2']
