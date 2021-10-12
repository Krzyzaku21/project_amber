from rest_framework import generics
from ..serializers import RegisterSerializer, EmailVerifiSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CreateUser
from rest_framework_simplejwt.tokens import RefreshToken
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from django.shortcuts import render
from django.urls import reverse
from ..utils import Util
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
import jwt
from django.conf import settings


class IsAuthenticatedOrWriteOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        WRITE_METHODS = ["POST", ]

        return (
            request.method in WRITE_METHODS or
            request.user and
            request.user.is_authenticated
        )


class RegisterAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    serializer_class = RegisterSerializer
    style = {'template_pack': 'rest_framework/vertical/'}
    template_name = "accounts/register_panel.html"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CreateUser.objects.get(email=serializer.data['email'])
            domain = get_current_site(request).domain
            context = {
                'token': str(RefreshToken.for_user(user).access_token),
                'domain': domain,
            }
            Util.send_mail(user.email, context)
            return Response(
                {'data': serializer.data, 'messages': 'Token send to email'},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = RegisterSerializer()
        context = {
            'register_form': serializer,
            'style': self.style,
        }
        return render(request, self.template_name, context)


class EmailVerifiAPI(generics.GenericAPIView):
    serializer_class = EmailVerifiSerializer
    template_name = "accounts/register_email_response.html"

    def get(self, request, token):
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user = CreateUser.objects.get(id=payload['user_id'])
        try:
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'messages': 'Successfully activated', 'user': user, })
        except jwt.ExpiredSignatureError:
            user.delete()
            return Response({'error': 'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            user.delete()
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    pass
