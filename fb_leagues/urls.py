from django.urls import path
from .views import user_leagues_view, league_detail_view, join_league_via_token, confirm_join_league, update_team_color, return_rule

urlpatterns = [
    path('', user_leagues_view, name='user_leagues'),
    path('<int:league_id>/', league_detail_view, name='league_detail'),
    path('invite/<str:token>/', join_league_via_token, name='league_invite'),
    path('invite/<str:token>/confirm/', confirm_join_league, name='league_invite_confirm'),
    path('league/<str:league_id>/update_team_color/', update_team_color, name='update_team_color'),
    path('rules/', return_rule, name='rules'),
]
