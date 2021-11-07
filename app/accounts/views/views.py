from rest_framework import generics
from accounts.serializers import (
    RegisterSerializer,
    EmailVerifiSerializer,
    LoginSerializer,
    LogoutSerializer
)
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CreateUser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.utils import Util
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, logout
import jwt
from django.conf import settings
from django.contrib import messages


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    style = {'template_pack': 'rest_framework/vertical/'}
    template_name = "accounts/register_panel.html"

    def post(self, request):
        if request.accepted_renderer.format == 'json':
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
                Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        elif request.accepted_renderer.format == 'html':
            if request.method == 'POST':
                form = RegisterSerializer(data=request.data)
                if form.is_valid():
                    form.save()
                    user = CreateUser.objects.get(email=form.data['email'])
                    domain = get_current_site(request).domain
                    context = {
                        'token': str(RefreshToken.for_user(user).access_token),
                        'domain': domain,
                    }
                    Util.send_mail(user.email, context)
                    messages.success(request, f'Your account has been created. You can check your email!')
                    return redirect('main:base')
            return Response({'serializer': form})

    def get_queryset(self):
        if self.request is None:
            return CreateUser.objects.none()
        return CreateUser.objects.all()

    def get(self, request):
        serializer = RegisterSerializer()
        if request.accepted_renderer.format == 'html':
            return render(request, self.template_name, {'serializer': serializer, 'style': self.style})
        if request.accepted_renderer.format == 'json':
            return Response({'data': serializer.data,
                            'messages': 'You got a email'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifiAPI(generics.GenericAPIView):
    serializer_class = EmailVerifiSerializer
    template_name = "accounts/register_email_response.html"
    token_parameters = [openapi.Parameter('token', in_=openapi.IN_PATH,
                                          description='Add token', type=openapi.TYPE_STRING, required=True)]

    @ swagger_auto_schema(manual_parameters=token_parameters)
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CreateUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    style = {'template_pack': 'rest_framework/vertical/'}
    template_name = "accounts/login_panel.html"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user is not None and user.tokens is not None:
            login(request, user)
            if request.accepted_renderer.format == 'html':
                messages.success(request, f'You are logged in')
                return HttpResponseRedirect(reverse(settings.MAIN_REDIRECT_URL))
            elif request.accepted_renderer.format == 'json':
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request is None:
            return CreateUser.objects.none()
        return CreateUser.objects.all()

    def get(self, request):
        serializer = LoginSerializer()
        if request.user.is_authenticated:
            return redirect(settings.MAIN_REDIRECT_URL)
        else:
            if request.accepted_renderer.format == 'html':
                return render(request, self.template_name, {'serializer': serializer, 'style': self.style})
            elif request.accepted_renderer.format == 'json':
                new_data = {
                    'messages': 'Logged in successfully'
                }
                new_data.update(serializer.data)
                return Response(new_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        if self.request is None:
            return CreateUser.objects.none()
        return CreateUser.objects.all()

    def get(self, request):
        if request.accepted_renderer.format == 'json':
            logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.accepted_renderer.format == 'html':
            logout(request)
            return HttpResponseRedirect(reverse(settings.MAIN_REDIRECT_URL))
