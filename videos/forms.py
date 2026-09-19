from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Video


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="이메일", required=True)
    username = forms.CharField(label="사용자명", max_length=150, help_text="이름이 아닌 로그인용 사용자명을 입력하세요.")

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "이 영상에 대한 댓글을 남겨주세요.",
            })
        }
        labels = {"content": "댓글"}

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if not content:
            raise forms.ValidationError("댓글 내용을 입력하세요.")
        return content


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["category", "title", "youtube_url", "description", "is_published"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "youtube_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://www.youtube.com/watch?v=..."}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
