from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import LeagueMembership, League, FantasyTeam
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def resolve_invite_token(token):
    for role in ['mod', 'player', 'viewer']:
        kwargs = {f'invite_token_{role}': token}
        league = League.objects.filter(**kwargs).first()
        if league:
            return league, role
    return None, None

@login_required
def join_league_via_token(request, token):
    league, role = resolve_invite_token(token)
    if not league:
        return render(request, 'fb_leagues/join_league_error.html', {'message': '邀請連結無效或已過期'})

    if LeagueMembership.objects.filter(user=request.user, league=league).exists():
        return league_detail_view(request, league_id=league.league_id)

    if role == 'viewer':
        return render(request, 'fb_leagues/join_league_viewer.html', {'league': league, 'token': token})

    # 檢查人數上限
    if LeagueMembership.objects.filter(league=league,role__in=['player', 'mod']).count() >= league.config.max_players:
        return render(request, 'fb_leagues/join_league_error.html', {'message': '聯盟人數已滿'})

    return render(request, 'fb_leagues/join_league_player.html', {'league': league, 'token': token, 'role': role})

@login_required
def confirm_join_league(request, token):
    league, role = resolve_invite_token(token)
    if not league:
        return render(request, 'fb_leagues/join_league_error.html', {'message': '邀請連結無效'})

    if LeagueMembership.objects.filter(user=request.user, league=league).exists():
        return league_detail_view(request, league_id=league.league_id)

    # 再次檢查人數
    if role in ['player', 'mod'] and LeagueMembership.objects.filter(league=league,role__in=['player', 'mod']).count() >= league.config.max_players:
        return render(request, 'fb_leagues/join_league_error.html', {'message': '聯盟人數已滿'})
    
    existing_team = LeagueMembership.objects.filter(league=league, user=request.user).first()

    if existing_team:
        messages.info(request, "您已擁有隊伍，無需再次建立。")
        return league_detail_view(request, league_id=league.league_id)
    
    LeagueMembership.objects.create(user=request.user, league=league, role=role)

    # 建立 FantasyTeam（僅 player / mod）
    if role in ['player', 'mod']:
        team_name = request.POST.get('team_name') or f"{request.user.username} 的隊伍"
        FantasyTeam.objects.create(
            league=league,
            owner=request.user,
            name=team_name
        )
    else:
        team_name = f'觀察者 {request.user.username}'
        messages.success(request, f"{team_name} 成功加入聯盟：{league.name}")
        return render(request, 'fb_leagues/join_success.html', {
        'league': league,
        'team': None
        })
    team = FantasyTeam.objects.get(league=league, owner=request.user)
    return render(request, 'fb_leagues/join_success.html', {
        'league': league,
        'team': team
    })

def user_leagues_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login'))

    memberships = LeagueMembership.objects.filter(user=user).select_related('league')
    leagues = [{
        'league': m.league,
        'role': m.get_role_display(),
        'joined_at': m.joined_at
    } for m in memberships]

    return render(request, 'fb_leagues/user_leagues.html', {'leagues': leagues,'segment': 'user_leagues'})

def league_detail_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)

    if not league.is_public:
        # 非公開聯盟 → 需要登入且是成員
        if not request.user.is_authenticated:
            return redirect(reverse('login'))  # 或顯示錯誤頁

        is_member = LeagueMembership.objects.filter(user=request.user, league=league).exists()
        if not is_member:
            return render(request, 'fb_leagues/access_denied.html', {
                'message': '此聯盟為非公開，僅限成員可瀏覽。'
            })

    teams = FantasyTeam.objects.filter(league=league).select_related('owner')
    memberships = LeagueMembership.objects.filter(league=league).select_related('user')
    return render(request, 'fb_leagues/league_detail.html', {
    'league': league,
    'teams': teams,
    'memberships': memberships,
    'invite_links': {
    'mod': request.build_absolute_uri(league.get_invite_url('mod')),
    'player': request.build_absolute_uri(league.get_invite_url('player')),
    'viewer': request.build_absolute_uri(league.get_invite_url('viewer')),
    }
    })
