from urllib.parse import parse_qs, urlparse
import re

from django.contrib.auth.models import User
from django.db import models


def extract_youtube_id(url: str) -> str:
    """일반 watch, youtu.be, shorts, embed URL에서 YouTube video ID를 추출합니다."""
    if not url:
        return ""

    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().split(":")[0]
    path = parsed.path.strip("/")

    if host in {"youtu.be", "www.youtu.be"}:
        return path.split("/")[0][:20]

    if "youtube.com" in host:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [""])[0][:20]
        for prefix in ("embed/", "shorts/", "live/"):
            if path.startswith(prefix):
                return path.split("/")[1][:20]

    match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{6,20})", url)
    return match.group(1) if match else ""


class Category(models.Model):
    name = models.CharField("카테고리명", max_length=100, unique=True)
    description = models.CharField("설명", max_length=255, blank=True)
    is_active = models.BooleanField("사용", default=True)
    created_at = models.DateTimeField("등록일", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리"

    def __str__(self):
        return self.name


class Video(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="videos", verbose_name="카테고리")
    title = models.CharField("제목", max_length=255)
    youtube_url = models.URLField("YouTube URL", max_length=500)
    youtube_id = models.CharField("YouTube ID", max_length=50, editable=False, db_index=True)
    description = models.TextField("설명", blank=True)
    is_published = models.BooleanField("공개", default=True)
    view_count = models.PositiveIntegerField("조회수", default=0)
    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "영상"
        verbose_name_plural = "영상"

    def save(self, *args, **kwargs):
        self.youtube_id = extract_youtube_id(self.youtube_url)
        if not self.youtube_id:
            from django.core.exceptions import ValidationError
            raise ValidationError({"youtube_url": "유효한 YouTube URL을 입력하세요."})
        super().save(*args, **kwargs)

    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}"

    @property
    def thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"

    def __str__(self):
        return self.title


class VideoLike(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes", verbose_name="영상")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_likes", verbose_name="회원")
    created_at = models.DateTimeField("등록일", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["video", "user"], name="unique_video_like_per_user")
        ]
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요"

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments", verbose_name="영상")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_comments", verbose_name="회원")
    content = models.TextField("댓글", max_length=1000)
    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["video", "user"], name="unique_video_comment_per_user")
        ]
        verbose_name = "댓글"
        verbose_name_plural = "댓글"

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"
