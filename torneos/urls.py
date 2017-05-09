from django.conf.urls import url

from .views import torneo_views
from .views.registration_views import RegistrationView
from .views.score_views import ScoreView
from .views import profile_view

app_name = "torneos"
urlpatterns = [
	url(r'^profile/$',  torneo_views.update_profile, name="profile"),
	url(r'^signup/$', profile_view.signup, name='signup'),

    url(r'^account_activation_sent/$', profile_view.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        profile_view.activate, name='activate'),
	
	url(r'^competiciones/$', torneo_views.index, name='index'),
	url(r'^competiciones/(?P<torneo_id>[0-9]+)/$', torneo_views.detail, name='torneos_detail'),
	url(r'^competiciones/(?P<torneo_id>[0-9]+)/(?P<slug>[-\w]+)/$',  
		torneo_views.TorneoDetailView.as_view(), 
		name="torneos_detail_slug"),

    url(r'^competiciones/(?P<torneo_id>[0-9]+)/(?P<slug>[\w-]+)/register/$',
        RegistrationView.as_view(),
        name='register_for'),

    url(r'^competiciones/(?P<torneo_id>[0-9]+)/(?P<slug>[\w-]+)/submission/$',
        ScoreView.as_view(),
        name='submission_for'),
]

