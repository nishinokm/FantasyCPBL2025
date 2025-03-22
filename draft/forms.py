# draft/forms.py
from django import forms
from .models import DraftRoom

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