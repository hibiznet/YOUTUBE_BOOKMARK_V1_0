from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency("auth.User"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="카테고리명")),
                ("description", models.CharField(blank=True, max_length=255, verbose_name="설명")),
                ("is_active", models.BooleanField(default=True, verbose_name="사용")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="등록일")),
            ],
            options={
                "verbose_name": "카테고리",
                "verbose_name_plural": "카테고리",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="제목")),
                ("youtube_url", models.URLField(max_length=500, verbose_name="YouTube URL")),
                ("youtube_id", models.CharField(db_index=True, editable=False, max_length=50, verbose_name="YouTube ID")),
                ("description", models.TextField(blank=True, verbose_name="설명")),
                ("is_published", models.BooleanField(default=True, verbose_name="공개")),
                ("view_count", models.PositiveIntegerField(default=0, verbose_name="조회수")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="등록일")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="videos", to="videos.category", verbose_name="카테고리")),
            ],
            options={
                "verbose_name": "영상",
                "verbose_name_plural": "영상",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="VideoLike",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="등록일")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="video_likes", to="auth.user", verbose_name="회원")),
                ("video", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="videos.video", verbose_name="영상")),
            ],
            options={
                "verbose_name": "좋아요",
                "verbose_name_plural": "좋아요",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(max_length=1000, verbose_name="댓글")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="등록일")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="video_comments", to="auth.user", verbose_name="회원")),
                ("video", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="videos.video", verbose_name="영상")),
            ],
            options={
                "verbose_name": "댓글",
                "verbose_name_plural": "댓글",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="videolike",
            constraint=models.UniqueConstraint(fields=("video", "user"), name="unique_video_like_per_user"),
        ),
        migrations.AddConstraint(
            model_name="comment",
            constraint=models.UniqueConstraint(fields=("video", "user"), name="unique_video_comment_per_user"),
        ),
    ]
