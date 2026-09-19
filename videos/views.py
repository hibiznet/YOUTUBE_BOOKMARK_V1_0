from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CommentForm, SignupForm
from .models import Category, Comment, Video, VideoLike


def home(request):
    categories = Category.objects.filter(is_active=True).annotate(video_count=Count("videos"))
    selected_category_id = request.GET.get("category")

    videos = Video.objects.filter(
        is_published=True,
        category__is_active=True,
    ).select_related("category")

    selected_category = None
    if selected_category_id:
        try:
            selected_category = categories.get(pk=selected_category_id)
            videos = videos.filter(category=selected_category)
        except (Category.DoesNotExist, ValueError):
            pass

    context = {
        "categories": categories,
        "videos": videos,
        "selected_category": selected_category,
    }
    return render(request, "videos/home.html", context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id, is_active=True)
    videos = Video.objects.filter(
        category=category,
        is_published=True,
    ).select_related("category")
    return render(request, "videos/category.html", {"category": category, "videos": videos})


def video_detail(request, pk):
    video = get_object_or_404(
        Video.objects.select_related("category"),
        pk=pk,
        is_published=True,
        category__is_active=True,
    )

    Video.objects.filter(pk=video.pk).update(view_count=video.view_count + 1)
    video.view_count += 1

    liked = request.user.is_authenticated and VideoLike.objects.filter(
        video=video, user=request.user
    ).exists()

    existing_comment = None
    if request.user.is_authenticated:
        existing_comment = Comment.objects.filter(video=video, user=request.user).first()

    comments = video.comments.select_related("user").all()
    form = CommentForm()

    return render(
        request,
        "videos/detail.html",
        {
            "video": video,
            "liked": liked,
            "comments": comments,
            "existing_comment": existing_comment,
            "comment_form": form,
        },
    )


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect("home")
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
@require_POST
def toggle_like(request, pk):
    video = get_object_or_404(Video, pk=pk, is_published=True)
    like, created = VideoLike.objects.get_or_create(video=video, user=request.user)
    if not created:
        like.delete()
        messages.info(request, "좋아요를 취소했습니다.")
    else:
        messages.success(request, "좋아요를 등록했습니다.")
    return redirect("video_detail", pk=pk)


@login_required
@require_POST
def add_comment(request, pk):
    video = get_object_or_404(Video, pk=pk, is_published=True)
    if Comment.objects.filter(video=video, user=request.user).exists():
        messages.warning(request, "이 영상에는 이미 댓글을 등록하셨습니다.")
        return redirect("video_detail", pk=pk)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.video = video
        comment.user = request.user
        try:
            comment.save()
            messages.success(request, "댓글이 등록되었습니다.")
        except IntegrityError:
            messages.warning(request, "이미 댓글이 등록되어 있습니다.")
    else:
        for error in form.errors.get("content", []):
            messages.error(request, error)

    return redirect("video_detail", pk=pk)


@login_required
@require_POST
def delete_comment(request, pk):
    video = get_object_or_404(Video, pk=pk)
    comment = get_object_or_404(Comment, pk=request.POST.get("comment_id"), video=video, user=request.user)
    comment.delete()
    messages.success(request, "댓글을 삭제했습니다.")
    return redirect("video_detail", pk=pk)
