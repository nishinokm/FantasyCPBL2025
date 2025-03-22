
from django.urls import path
from . import views

urlpatterns = [
    path('<int:league_id>/draft/', views.draft_room_view, name='draft_room'),
    path('<int:league_id>/draft/create/', views.create_draft_room_view, name='create_draft_room'),
]