from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from ..utils import get_register_add, post_register_add
# Create your views here.


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return get_register_add(request)

    if request.method == 'POST':
        return post_register_add(request)
