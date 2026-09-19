from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("video/<int:pk>/", views.video_detail, name="video_detail"),
    path("video/<int:pk>/like/", views.toggle_like, name="toggle_like"),
    path("video/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("video/<int:pk>/comment/delete/", views.delete_comment, name="delete_comment"),
]
