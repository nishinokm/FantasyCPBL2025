# draft/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from fb_leagues.models import League, LeagueMembership
from .models import DraftRoom
from .forms import DraftRoomCreateForm

@login_required
def create_draft_room_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)
    
    # 檢查權限：只有 mod 或 owner 可建立
    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership or membership.role not in ['owner', 'mod']:
        return render(request, 'fb_leagues/access_denied.html', {
            'message': '只有擁有者或管理員可以建立選秀房。'
        })

    if hasattr(league, 'draft_room'):
        return redirect('draft_room', league_id=league.league_id)

    if request.method == 'POST':
        form = DraftRoomCreateForm(request.POST)
        if form.is_valid():
            draft = form.save(commit=False)
            draft.league = league
            draft.save()
            return redirect('draft_room', league_id=league.league_id)
    else:
        form = DraftRoomCreateForm()

    return render(request, 'draft/create_draft_room.html', {
        'league': league,
        'form': form
    })

def draft_room_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)

    # 如果沒有 DraftRoom 就建立一個（可選）
    draft, created = DraftRoom.objects.get_or_create(
        league=league,
        defaults={'draft_type': 'snake'}
    )

    return render(request, 'draft/draft_room.html', {
        'league': league,
        'draft': draft,
        'created': created,
    })