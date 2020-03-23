from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.shortcuts import redirect
from django.urls import reverse

from base.admin import stable_admin
from users.forms import AdminManualQuoteUserForm
from users.proxy_models import ManualQuoteUser
from users.models import User, ResetPasswordLink


class UserAdmin(DjangoUserAdmin):
    """ Admin model for custom User model with no email field """

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-modified", "-created", "email", )


stable_admin.register(User, UserAdmin)
admin.site.register(User, UserAdmin)


class ManualQuoteUserAdmin(admin.ModelAdmin):
    form = AdminManualQuoteUserForm

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     if object_id:
    #         return redirect(reverse('stable_admin:index'))
    #     else:
    #         return super(ManualQuoteUserAdmin, self).change_view(
    #             request, object_id, form_url='', extra_context=None
    #         )

    # def changelist_view(self, request, extra_context=None):
    #     return redirect(reverse('stable_admin:index'))

    def get_form(self, request, obj=None, **kwargs):
        form = super(ManualQuoteUserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['quote_process'].initial = request.GET.get('quote_process')
        return form

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_add(self, request, obj):
        quote_process = obj.quote_process
        return redirect(
            reverse('stable_admin:quote_quoteprocess_change', args=(quote_process.id, ))
        )

stable_admin.register(ManualQuoteUser, ManualQuoteUserAdmin)
stable_admin.register(ResetPasswordLink)