from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'profile_picture', 'short_description')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'short_description'),
        }),
    )
    list_display = ('id', 'email', 'name', 'is_valid', 'is_superuser', 'created_at')
    list_filter = ('is_valid', 'is_superuser')
    search_fields = ('email', 'name')
    ordering = ('-created_at', 'email')

    # Adding a custom action to mark users as valid
    def make_valid(self, request, queryset):
        updated_count = queryset.update(is_valid=True)
        self.message_user(request, f"{updated_count} user(s) were successfully marked as valid.")

    actions = [make_valid]


admin.site.register(CustomUser, CustomUserAdmin)
