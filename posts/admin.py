from django.contrib import admin

from posts.models import Post


@admin.action(description='Restore selected soft-deleted posts')
def restore_posts(modeladmin, request, queryset):
    for post in queryset:
        post.restore()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'deleted_at')
    list_filter = ('deleted_at', 'author', 'created_at')
    actions = [restore_posts]
