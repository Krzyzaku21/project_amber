from ..utils import get_register, post_register
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from ..serializers import RegisterSerializer


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        return get_register(request)

    def post(self, request):
        return post_register(request)
