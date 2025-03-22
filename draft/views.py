# draft/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from fb_leagues.models import League, LeagueMembership, FantasyTeam
from .models import DraftRoom, DraftUnit
from .forms import DraftRoomCreateForm, PreDraftPickFormSet
from django.contrib import messages

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
        formset = PreDraftPickFormSet(request.POST, prefix='form')
        order = request.POST.getlist("draft_order")

        if not order or len(order) != teams.count():
            order_error = True
            messages.error(request, "請排序所有隊伍後再建立選秀房。")
        elif form.is_valid() and formset.is_valid():
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

            messages.success(request, "選秀房與預選順位已建立成功！")
            return redirect('draft_room', league_id=league_id)
    else:
        form = DraftRoomCreateForm()
        formset = PreDraftPickFormSet(prefix='form', queryset=DraftUnit.objects.none())

    return render(request, 'draft/create_draft_room.html', {
        'league': league,
        'form': form,
        'formset': formset,
        'teams': teams,
        'order_error': order_error,
    })

@login_required
def draft_room_view(request, league_id):
    league = get_object_or_404(League, league_id=league_id)
    draft = get_object_or_404(DraftRoom, league=league)

    # ✅ 權限：若非公開，僅允許成員進入
    if not league.is_public:
        if not league.members.filter(id=request.user.id).exists():
            return render(request, 'fb_leagues/access_denied.html', {
                'message': '此聯盟為非公開，僅限成員可查看選秀房。'
            })

    draft_units = DraftUnit.objects.filter(draft=draft).select_related(
        'player', 'ori_owner', 'new_owner'
    ).order_by('round', 'pick')

    return render(request, 'draft/draft_room.html', {
        'league': league,
        'draft': draft,
        'units': draft_units
    })