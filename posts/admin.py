from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['author', 'content']}),)
    list_display = ('id', 'author', 'created_at', 'deleted_at')
    list_filter = ('deleted_at', 'author', 'created_at')
    ordering = ('-created_at',)

    def restore_posts(self, request, queryset):
        resotred_count = queryset.update(deleted_at=None)
        self.message_user(request, f"{resotred_count} post(s) were successfully restored.")

    actions = [restore_posts]


admin.site.register(Post, PostAdmin)
