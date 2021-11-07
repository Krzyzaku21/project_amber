from rest_framework import serializers, status
from accounts.models import CreateUser
from django.contrib.auth import authenticate, logout
from django.utils.translation import ugettext_lazy as _translate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, min_length=8,
                                     max_length=20, style={'input_type': 'password'})
    password2 = serializers.CharField(required=True, write_only=True, min_length=8,
                                      max_length=20, style={'input_type': 'password'})

    class Meta:
        model = CreateUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'username', 'password', 'password2', 'avatar']

    def validate(self, validated_data):
        symbols = ['$', '@', '#', '%', '!']
        errors = dict()
        password1 = validated_data.get('password')
        password2 = validated_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                errors['password'] = "Passwords don\'t match."
                raise serializers.ValidationError(errors)
            else:
                if not any(symbol in symbols for symbol in password1):
                    errors['password'] = f"Passwords don\'t have symbols like {symbols}"
                    raise serializers.ValidationError(errors)
                if not any(char.isdigit() for char in password1):
                    errors['password'] = 'Password should have at least one numeral'
                    raise serializers.ValidationError(errors)
                if not any(char.isupper() for char in password1):
                    errors['password'] = 'Password should have at least one uppercase letter'
                    raise serializers.ValidationError(errors)
                if not any(char.islower() for char in password1):
                    errors['password'] = 'Password should have at least one lowercase letter'
                    raise serializers.ValidationError(errors)

        return super(RegisterSerializer, self).validate(validated_data)

    def validate_email(self, email):
        if CreateUser.objects.filter(email=email).exists():
            msg = _translate("User with that email exists.")
            raise serializers.ValidationError({'password': msg})
        return email

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


class EmailVerifiSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CreateUser
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=10, max_length=45, required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={'input_type': 'password'},
        label=_translate('Password'))
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, attrs):
        user = CreateUser.objects.get(email=attrs['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = CreateUser
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                msg = _translate('Bad user authorization')
                raise serializers.ValidationError(msg)
            if not user.is_active:
                msg = _translate('User is not active')
                raise serializers.ValidationError(msg)
            if not user.is_verified:
                msg = _translate('Email is not verified')
                raise serializers.ValidationError(msg)
            else:
                return {
                    'user': user,
                    'email': user.email,
                    'tokens': user.tokens,
                }
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
