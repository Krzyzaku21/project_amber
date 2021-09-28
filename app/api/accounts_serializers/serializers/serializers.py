from rest_framework import serializers
from accounts.models import CreateUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password', 'password2', 'avatar']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def save(self):
        createuser = CreateUser(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        createuser.set_password(self.validated_data['password'])
        createuser.save()
        return createuser
