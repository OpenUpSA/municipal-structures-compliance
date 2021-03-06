import secrets
import string

from django.contrib import admin

from django.conf import settings

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
# Register your models here.

from .models import User, Share
from .forms import CustomUserCreationForm, CustomUserChangeForm

from msc.organisation.models import EmailActivity


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'organisation', 'is_staff',)
    list_filter = ('is_staff', 'organisation', 'is_superuser',)


    change_fieldsets = (
        (None, {'fields': ('email', 'organisation')}),
        ("Personal info", {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    superuser_fieldsets = (
        (None, {'fields': ('email', 'password', 'organisation')}),
        ("Personal info", {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'organisation', 'is_admin',),
        }),
    )

    super_user_add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'organisation', 'is_admin', 'send_email'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ("is_staff",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form


    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            if request.user.is_superuser:
                return self.superuser_fieldsets
            return self.change_fieldsets

        else:
            if request.user.is_superuser:
                return self.super_user_add_fieldsets
        return self.add_fieldsets

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organisation":
            if not request.user.is_superuser:
                kwargs["queryset"] = request.user.organisation.get_children()
            kwargs["initial"] = request.user.organisation
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        add_as_admin = form.cleaned_data.get("is_admin", False)
        obj.is_staff = add_as_admin or obj.is_superuser
        send_email = form.cleaned_data.get("send_email", True)
        if "groups" in form.cleaned_data:
            if not obj.organisation or not add_as_admin:
                form.cleaned_data["groups"] = []
            elif obj.organisation and add_as_admin:
                group_name = "Admin"
                if not obj.organisation.parent:
                    group_name = "SuperAdmin"
                group = Group.objects.get(name=group_name)
                form.cleaned_data["groups"] = [group]

        super().save_model(request, obj, form, change)

        if "groups" not in form.cleaned_data and obj.organisation:
            group_name = "Admin"
            if not obj.organisation.parent:
                group_name = "SuperAdmin"
            group = Group.objects.get(name=group_name)
            if add_as_admin:
                obj.groups.add(group)
            elif not add_as_admin:
                obj.groups.remove(group)

        if not change and send_email:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(15))
            obj.set_password(password)
            obj.username = obj.email.split("@")[0]
            obj.save()

            activity = EmailActivity.objects.create(
                activity_type="account_activation", user=request.user
            )
            activity.to_users.add(obj)
            activity.send_email(
                request, password=password, email=obj.email, obj=obj
            )


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return queryset

        if user.is_national:
            return queryset.exclude(is_superuser=True)

        organisations = user.organisation.get_children()
        return queryset.filter(organisation__in=organisations)

admin.site.register(User, UserAdmin)


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    model = Share
    list_display = ('target', 'sharer', 'shared_by', 'relationship')
    list_filter = ('shared_by', 'relationship')