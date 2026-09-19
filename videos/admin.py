from django.contrib import admin
from .models import Category, Comment, Video, VideoLike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "video_count", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="영상 수")
    def video_count(self, obj):
        return obj.videos.count()


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "view_count", "like_count", "comment_count", "created_at")
    list_filter = ("category", "is_published", "created_at")
    search_fields = ("title", "youtube_url", "youtube_id")
    readonly_fields = ("youtube_id", "view_count", "created_at", "updated_at")
    list_select_related = ("category",)

    @admin.display(description="좋아요")
    def like_count(self, obj):
        return obj.likes.count()

    @admin.display(description="댓글")
    def comment_count(self, obj):
        return obj.comments.count()


@admin.register(VideoLike)
class VideoLikeAdmin(admin.ModelAdmin):
    list_display = ("video", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("video__title", "user__username", "user__email")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("video", "user", "short_content", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("video__title", "user__username", "content")

    @admin.display(description="댓글")
    def short_content(self, obj):
        return obj.content[:80]
