from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import RegisterUserForm, RegisterChangeForm
from .models import CreateUser

# Register your models here.


class AdminUser(BaseUserAdmin):
    form = RegisterChangeForm
    add_form = RegisterUserForm

    list_display = ['first_name', 'last_name', 'date_of_birth', 'email',
                    'password', 'password2', 'avatar', 'is_active', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = [
        [None, {'fields': ['email', 'password']}],
        ['Personal info', {'fields': ['date_of_birth', ]}],
        ['Permissions', {'fields': ['is_admin', ]}],
    ]
    add_fieldsets = [
        [None, {
            'classes': ['wide', ],
            'fields': ['email', 'date_of_birth', 'password', 'password2']}
         ],
    ]
    search_fields = ['email', ]
    ordering = ['email', ]
    filter_horizontal = []


admin.site.register(CreateUser, AdminUser)
admin.site.unregister(Group)