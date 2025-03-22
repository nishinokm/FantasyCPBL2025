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
        team_color = request.POST.get('team_color') or f"#000000"
        FantasyTeam.objects.create(
            league=league,
            owner=request.user,
            name=team_name,
            color=team_color
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
    joined_league_ids = memberships.values_list('league__league_id', flat=True)

    # 顯示所有公開聯盟（不包含已加入的）
    public_leagues = League.objects.filter(is_public=True).exclude(league_id__in=joined_league_ids)
    leagues = [{
        'league': m.league,
        'role': m.get_role_display(),
        'joined_at': m.joined_at
    } for m in memberships]

    return render(request, 'fb_leagues/user_leagues.html', {
        'leagues': leagues,
        'public_leagues': public_leagues,
        'segment': 'user_leagues'
    })

def league_detail_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)
    user = request.user

    # 全部會員 & 所有隊伍一次查好
    memberships = LeagueMembership.objects.filter(league=league).select_related('user')
    teams = FantasyTeam.objects.filter(league=league).select_related('owner')

    # 預設使用者狀態
    is_member = False
    user_role = None

    if user.is_authenticated:
        user_membership = memberships.filter(user=user).first()
        if user_membership:
            is_member = True
            user_role = user_membership.role

    # 非公開聯盟檢查權限
    if not league.is_public and not is_member:
        if not user.is_authenticated:
            return redirect(reverse('login'))
        return render(request, 'fb_leagues/access_denied.html', {
            'message': '此聯盟為非公開，僅限成員可瀏覽。'
        })

    # 根據身分顯示邀請連結
    invite_links = {}
    if user_role == 'viewer':
        invite_links['viewer'] = request.build_absolute_uri(league.get_invite_url('viewer'))
    elif user_role == 'player'or not is_member:
        invite_links['viewer'] = request.build_absolute_uri(league.get_invite_url('viewer'))
        invite_links['player'] = request.build_absolute_uri(league.get_invite_url('player'))
    elif user_role in ['mod', 'owner']:
        # 給管理員或尚未加入者看全部（讓未加入者可以取得 player 連結用於加入）
        invite_links['mod'] = request.build_absolute_uri(league.get_invite_url('mod'))
        invite_links['player'] = request.build_absolute_uri(league.get_invite_url('player'))
        invite_links['viewer'] = request.build_absolute_uri(league.get_invite_url('viewer'))

    return render(request, 'fb_leagues/league_detail.html', {
        'league': league,
        'teams': teams,
        'memberships': memberships,
        'invite_links': invite_links,
        'is_member': is_member,
        'user_role': user_role,
    })