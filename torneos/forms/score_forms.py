from django import forms
from django.contrib.auth.models import User
from ..models.score_model import Score
from ..models.torneo_model import Torneo


class ScoreForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
            widget=forms.HiddenInput())
    competition = forms.ModelChoiceField(queryset=Torneo.objects.all(),
            widget=forms.HiddenInput())

    score = forms.CharField(widget = forms.HiddenInput(), required = False)
    error = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Score
        fields = ('description', 'document')
