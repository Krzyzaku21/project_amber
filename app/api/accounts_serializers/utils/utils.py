from rest_framework.response import Response
from ..serializers import RegisterSerializer
from accounts.models import CreateUser
from rest_framework import status


def get_register(request):
    try:
        register = CreateUser.objects.all()
        serializer = RegisterSerializer(register, many=True)
        return Response(serializer.data)
    except CreateUser.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


def post_register(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['date_of_birth'] = account.date_of_birth
            data['username'] = account.username
            data['email'] = account.email
            data['avatar'] = account.avatar
            data['password'] = account.password
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CreateUser.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
