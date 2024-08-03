from django.contrib import admin

from posts.models import Post


@admin.action(description='Restore selected soft-deletedposts')
def restore_posts(modeladmin, request, queryset):
    for post in queryset:
        post.restore()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('author', 'created_at', 'updated_at', 'deleted_at')
    actions = [restore_posts]
