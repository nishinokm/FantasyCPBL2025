# draft/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from fb_leagues.models import League, LeagueMembership, FantasyTeam
from .models import DraftRoom, DraftUnit
from .forms import DraftRoomCreateForm, PreDraftPickFormSet, SwapDraftPickFormSet
from cpbl_players.models import CPBLPlayer
import json
from collections import defaultdict

@login_required
def create_draft_room_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)

    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership or membership.role not in ['owner', 'mod']:
        return render(request, 'fb_leagues/access_denied.html', {
            'message': '只有擁有者或管理員可以建立選秀房。'
        })

    if hasattr(league, 'draft_room'):
        return redirect('draft_room', league_id=league_id)

    teams = FantasyTeam.objects.filter(league=league)
    order_error = False

    if request.method == 'POST':
        form = DraftRoomCreateForm(request.POST)
        formset = PreDraftPickFormSet(request.POST, prefix='form',form_kwargs={'teams': teams} )
        order = request.POST.getlist("draft_order")
        swap_formset = SwapDraftPickFormSet(request.POST, prefix='swap')

        if not order or len(order) != teams.count():
            order_error = True
            messages.error(request, "請排序所有隊伍後再建立選秀房。")
        elif form.is_valid() and formset.is_valid() and swap_formset.is_valid():
            draft = form.save(commit=False)
            draft.league = league
            draft.save()

            for unit in formset.save(commit=False):
                unit.draft = draft
                unit.pre_draft = True
                unit.new_owner = unit.ori_owner
                unit.save()

            max_draft_rounds = form.cleaned_data.get('max_round', 1)
            for round_num in range(1, max_draft_rounds + 1):
                for i, team_id in enumerate(order):
                    pick_num = i + 1
                    if DraftUnit.objects.filter(draft=draft, round=round_num, pick=pick_num).exists():
                        continue
                    team = FantasyTeam.objects.get(pk=team_id)
                    DraftUnit.objects.create(
                        draft=draft,
                        round=round_num,
                        pick=pick_num,
                        ori_owner=team,
                        new_owner=team
                    )

            for swap in swap_formset.cleaned_data:
                if not swap or swap.get('DELETE'):
                    continue
                
                round_a = swap['round_a']
                pick_a = swap['pick_a']
                round_b = swap['round_b']
                pick_b = swap['pick_b']

                unit_a = DraftUnit.objects.filter(draft=draft,round=round_a, pick=pick_a).first()
                unit_b = DraftUnit.objects.filter(draft=draft,round=round_b, pick=pick_b).first()

                if unit_a and unit_b:
                    unit_a.new_owner, unit_b.new_owner = unit_b.ori_owner, unit_a.ori_owner
                    unit_a.save()
                    unit_b.save()

            messages.success(request, "選秀房與交換順位已建立")
            return redirect('draft_room', league_id=league_id)
    else:
        form = DraftRoomCreateForm()
        formset = PreDraftPickFormSet(prefix='form', queryset=DraftUnit.objects.none(),form_kwargs={'teams': teams} )
        swap_formset = SwapDraftPickFormSet(prefix='swap')

    return render(request, 'draft/create_draft_room.html', {
        'league': league,
        'form': form,
        'formset': formset,
        'swap_formset': swap_formset,
        'teams': teams,
        'order_error': order_error,
    })

@login_required
def draft_room_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)
    draft = get_object_or_404(DraftRoom, league=league)

    if not league.is_public and not league.members.filter(id=request.user.id).exists():
        return render(request, 'fb_leagues/access_denied.html', {
            'message': '此聯盟為非公開，僅限成員可查看選秀房。'
        })

    return render(request, 'draft/draft_room.html', {
        'league': league,
        'draft': draft,
    })
@login_required
@require_GET
def draft_snapshot(request, draft_id):

    draft = get_object_or_404(DraftRoom, id=draft_id)
    update_draft_position(draft)
    units = DraftUnit.objects.filter(draft=draft).select_related('ori_owner', 'new_owner', 'player').order_by('round', 'pick')
    picked_ids = [u.player.id for u in units if u.player]
    available_players = CPBLPlayer.objects.exclude(id__in=picked_ids).order_by('name')

    current_unit = DraftUnit.objects.filter(
        draft=draft,
        round=draft.current_round,
        pick=draft.current_pick,
    ).select_related('new_owner__owner').first()
    
    return JsonResponse({
        "current_round": draft.current_round,
        "current_pick": draft.current_pick,
        "current_owner": current_unit.new_owner.name if current_unit else "未知",
        "current_owner_color": current_unit.new_owner.color if current_unit else "#f0f0f0",
        "current_owner_text_color": current_unit.new_owner.text_color if current_unit else "#0f0f0f",
        "is_your_turn": current_unit and current_unit.new_owner.owner_id == request.user.id,
        "is_complete": draft.is_complete,
        "units": group_units_by_round(units),
        "available_players": [
            {"id": p.id, "name": p.name, "main_pos": p.main_pos, 'team_id':p.team_id} for p in available_players
        ]
    })

def group_units_by_round(units):
    grouped = defaultdict(list)
    for u in units:
        grouped[u.round].append({
            "player": u.player.name if u.player else "-",
            "team_id": u.player.team_id if u.player else None,
            "color": u.new_owner.color if u.new_owner.color else "#ffffff",
            "text_color": u.new_owner.text_color if u.new_owner.text_color else "#000000",
            "owner": u.new_owner.name,
            'main_pos': u.player.main_pos if u.player else "-"
        })
    return [{"round": r, "picks": picks} for r, picks in grouped.items()]

def update_draft_position(draft):
    """自動更新目前輪次與順位（支援 snake 順序）"""
    all_units = DraftUnit.objects.filter(draft=draft).order_by('round', 'pick')

    grouped_units = {}
    for unit in all_units:
        grouped_units.setdefault(unit.round, []).append(unit)

    # 依輪次排序，檢查每輪的順位是否有未選
    for round_num in sorted(grouped_units.keys()):
        units_in_round = grouped_units[round_num]

        # 若是 snake 模式，偶數輪倒著選
        if draft.draft_type == 'snake' and round_num % 2 == 0:
            units_in_round = list(reversed(units_in_round))

        for unit in units_in_round:
            if not unit.player:
                draft.current_round = unit.round
                draft.current_pick = unit.pick
                draft.save(update_fields=['current_round', 'current_pick'])
                return

    # 若都選完，標記完成
    draft.is_complete = True
    draft.save(update_fields=['is_complete'])

@csrf_exempt
@require_POST
def pick_player_api(request):
    data = json.loads(request.body)
    draft = DraftRoom.objects.get(id=data['draft_id'])
    player = CPBLPlayer.objects.get(id=data['player_id'])
    if draft.is_complete:
        return JsonResponse({"status": "error", "message": "選秀已結束"}, status=403)
    unit = DraftUnit.objects.filter(
        draft=draft,
        round=draft.current_round,
        pick=draft.current_pick,
        player__isnull=True
    ).select_related('new_owner__owner').first()

    if not unit or unit.new_owner.owner != request.user:
        return JsonResponse({"status": "error", "message": "不是你的輪次"}, status=403)

    unit.player = player
    unit.pick_at_time = now()
    unit.save()

    remaining_units = DraftUnit.objects.filter(draft=draft).order_by('round', 'pick')
    for u in remaining_units:
        if not u.player:
            draft.current_round = u.round
            draft.current_pick = u.pick
            draft.save()
            break
    else:
        draft.is_complete = True
        draft.save()

    return JsonResponse({"status": "ok"})