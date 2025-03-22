
from django.urls import path
from . import views

urlpatterns = [
    path('<int:league_id>/draft/', views.draft_room_view, name='draft_room'),
    path('<int:league_id>/draft/create/', views.create_draft_room_view, name='create_draft_room'),
    path('draft/<int:draft_id>/status/', views.current_draft_status, name='draft_status'),
    path('draft/<int:draft_id>/snapshot/', views.draft_snapshot, name='draft_snapshot'),
]