from rest_framework.decorators import api_view
from ..utils import get_register, post_register
from rest_framework.renderers import TemplateHTMLRenderer
# Create your views here.


@api_view(['GET', 'POST'])
def api_register(request):

    if request.method == 'GET':
        return get_register(request)

    if request.method == 'POST':
        return post_register(request)
