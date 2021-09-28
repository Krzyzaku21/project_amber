from ..forms import RegisterUserForm
from django.shortcuts import render, HttpResponse


def post_register_add(request):
    template_name = 'accounts/register.html'
    register_form = RegisterUserForm(request.POST)
    if register_form.is_valid():
        new_user = register_form.save(commit=False)
        new_user.set_password(register_form.cleaned_data['password'])
        new_user.save()
        return HttpResponse("You are registered")
    context = {
        'register_form': register_form,
    }
    return render(request, template_name, context)


def get_register_add(request):
    template_name = 'accounts/register.html'
    register_form = RegisterUserForm()
    context = {
        'register_form': register_form,
    }
    return render(request, template_name, context)
