from rest_framework import serializers
from accounts.models import CreateUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CreateUser.objects.all())]
            )
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password', 'password2', 'avatar']
        write_only_fields = ['password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def save(self):
        createuser = CreateUser(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            date_of_birth=self.validated_data['date_of_birth'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
        )
        createuser.set_password(self.validated_data['password'])
        createuser.save()
        return createuser