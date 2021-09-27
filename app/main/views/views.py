from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class HomepageView(View):
    def __init__(self):
        self.template_name = "main/base.html"
        self.context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)
