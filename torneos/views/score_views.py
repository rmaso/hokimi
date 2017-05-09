from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView, ProcessFormView
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import render
from ..pyhparser import pyhparser
from ..pyhparser.utils import readFile

from .mixins import (LoggedInMixin, TorneoViewMixin,
                                      UserRegisteredMixin, # ConfirmationMixin,
                                      RequireOpenMixin)

from ..forms.score_forms import ScoreForm

import sys
import hokimicms.settings as s

#LoggedInMixin,
#TorneoViewMixin,
                       
class ScoreView(UserRegisteredMixin,
                       RequireOpenMixin,
                       TemplateResponseMixin,
                       ProcessFormView):
    """Allows a user to register to compete"""
    template_name = 'torneos/submission_upload.html'

    def user_is_registered(self):
        """Returns True if a user already has an **active**
        registration for the competition corresponding to comp_slug,
        otherwise returns False."""
        return self.get_torneo().is_user_registered(self.request.user)

    def get(self, request, *_args, **_kwargs):
        """This method is called when a user performs a GET request to
        this view... namely, when they load the form."""
        competition = self.get_torneo()

        # If the user's already registered, send them back to the
        # competition's page.
        if not (self.user_is_registered()):
            msg = "You're not already registered for %s" % competition.title
            messages.info(request, msg)
            return redirect('torneos:register_for', torneo_id=competition.t_id, slug=competition.slug)

        form = ScoreForm(initial={'user':request.user, 'competition': competition})

        return self.render_to_response({'form': form, 'competition': self.get_torneo()})


    def post(self, request, *_args, **_kwargs):
        """This method is called when a user performs a POST request
        to this view... namely, when the submit a filled in form"""
        competition = self.get_torneo()
        user = request.user

        form = ScoreForm(request.POST, request.FILES)
        if form.is_valid():
            score = form.save(commit=False)
            score.user = user
            score.competition = competition
            score.score=0
            score.error=""
            score.save()

            public_leaderboard_file = readFile(competition.public_leaderboard_file.name)
            #print >>sys.stderr, public_leaderboard_file
            #print >>sys.stderr, public_leaderboard_file.count("\n") + 1
            to_score_file = readFile(s.MEDIA_ROOT+"/"+score.document.name) # score.document
            #print >>sys.stderr, score.document
            #to_score_file = score.document.open()
            #tmp = to_score_file.open(mode="rb")
            print >>sys.stderr, to_score_file
            print >>sys.stderr, to_score_file.count("\n") + 1
            score.user = user


            return redirect('torneos:torneos_detail_slug', torneo_id=competition.t_id, slug=competition.slug)
