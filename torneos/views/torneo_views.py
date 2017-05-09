from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
from django.http import HttpResponse
from ..models.torneo_model import Torneo
from ..forms.profile_forms import UserForm, ProfileForm

def index(request):
	latest_list = Torneo.objects.order_by('end_date')
	context = {'latest_list': latest_list}
	return render(request, 'torneos/index.html', context)


def detail(request, torneo_id):
	#https://docs.djangoproject.com/es/1.10/intro/tutorial03/
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	return render(request, 'torneos/detail.html', {'torneo': torneo})

class TorneoDetailView(DetailView):
    """Shows details about a particular competition"""
    context_object_name = 'torneo_id'
    model = Torneo
    slug_url_kwarg = 'slug'
    template_name = 'torneos/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TorneoDetailView, self).get_context_data(**kwargs)
        competition = self.object
        user = self.request.user
        context['user_registered'] = competition.is_user_registered(user)
#         context['user_team'] = None
#         try:
#             if not user.is_anonymous():
#                 context['user_team'] = competition.team_set.get(members=user.pk)
#         except ObjectDoesNotExist:
#             pass
        return context


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('torneos:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
