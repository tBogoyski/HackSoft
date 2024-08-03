from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'profile_picture', 'short_description')}),
        (
            'Permissions',
            {'fields': ('is_valid', 'is_staff', 'is_superuser', 'user_permissions')}
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'is_valid', 'is_superuser')
    list_filter = ('is_valid', 'is_superuser')
    search_fields = ('email', 'name')
    ordering = ('email',)

    # Adding a custom action to mark users as valid
    def make_valid(self, request, queryset):
        updated_count = queryset.update(is_valid=True)
        self.message_user(request, f"{updated_count} user(s) were successfully marked as valid.")

    actions = [make_valid]


admin.site.register(CustomUser, CustomUserAdmin)
