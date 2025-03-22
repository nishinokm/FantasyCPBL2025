# draft/forms.py
from django import forms
from .models import DraftRoom, DraftUnit, CPBLPlayer
ROUND_CHOICES = [(i, f"{i} 輪") for i in range(1, 27)]
PICK_CHOICES = [(i, f"{i} 順位") for i in range(1, 9)]
class DraftRoomCreateForm(forms.ModelForm):
    class Meta:
        model = DraftRoom
        fields = ['draft_type', 'max_round', 'min_giveup_round', 'top_n_round_for_draw']
        labels = {
            'draft_type': '選秀類型',
            'max_round': '最多輪數',
            'min_giveup_round': '最早可放棄輪數',
            'top_n_round_for_draw': '前 N 輪抽籤',
        }
        widgets = {
            'draft_type': forms.Select(attrs={'class': 'form-select'}),
            'max_round': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_giveup_round': forms.NumberInput(attrs={'class': 'form-control'}),
            'top_n_round_for_draw': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PreDraftPickForm(forms.ModelForm):
    round = forms.ChoiceField(choices=ROUND_CHOICES, label="輪數")
    pick = forms.ChoiceField(choices=PICK_CHOICES, label="順位")

    class Meta:
        model = DraftUnit
        fields = ['round', 'pick', 'ori_owner', 'player']
        labels = {
            'round': '輪數',
            'pick': '順位',
            'ori_owner': '原始隊伍',
            'player': '選擇球員'
        }

        widgets = {
            'player': forms.Select(attrs={
                'class': 'form-select select2',  # 對應 js 套件
                'data-placeholder': '搜尋球員名稱...'
            }),
            'ori_owner': forms.Select(attrs={'class': 'form-select'}),
        }

# formset 定義
PreDraftPickFormSet = forms.modelformset_factory(
    DraftUnit,
    form=PreDraftPickForm,
    extra=0,
    can_delete=True
)

class SwapDraftUnitOwnerForm(forms.Form):
    round_a = forms.ChoiceField(choices=ROUND_CHOICES, label="輪次 A")
    pick_a = forms.ChoiceField(choices=PICK_CHOICES, label="順位 A")
    round_b = forms.ChoiceField(choices=ROUND_CHOICES, label="輪次 B")
    pick_b = forms.ChoiceField(choices=PICK_CHOICES, label="順位 B")

SwapDraftPickFormSet = forms.formset_factory(SwapDraftUnitOwnerForm, extra=0, can_delete=True)