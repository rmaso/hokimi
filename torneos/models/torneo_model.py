from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

import hokimicms.settings as s

class TorneoManager(models.Manager):

	def user_registered(self, user):
		"""Returns competitions that the user is registered for"""
		if user.is_anonymous():
			return []
			return self.filter(registration__user=user.pk,
				registration__active=True)


class Torneo(models.Model):
	class Meta:
		app_label = 'torneos'


	t_id = models.AutoField(primary_key=True)
	title = models.CharField(blank=False, max_length=50)
	slug = models.SlugField(max_length=50)
	short_description = models.CharField(blank=False, max_length=200)
	image = models.ImageField(blank=False)
	long_description = HTMLField(blank=False)
	end_date = models.DateTimeField('end date', blank=False)
	prizes = HTMLField(blank=True)
	first_prize = models.CharField(blank=True, max_length=50)
	evaluation = HTMLField(blank=False)
	data = HTMLField(blank=False)
	recruiting = models.BooleanField()

	upload_storage = FileSystemStorage(location=s.BASE_DIR, base_url='/uploads')
	public_leaderboard_file = models.FileField(upload_to=s.BASE_DIR +'/torneos/leaderboard/public', storage=upload_storage)
	private_leaderboard_file = models.FileField(upload_to=s.BASE_DIR +'/torneos/leaderboard/private', storage=upload_storage)

	# Custom object manager
	objects = TorneoManager()

	questions = models.ManyToManyField("torneos.RegistrationQuestion", blank=True)

	@models.permalink
	def get_absolute_url(self):
		return ('torneos_detail_slug', (), {'torneo_id': self.t_id, 'slug': self.slug})

	def __str__(self):
		return u''.join((self.title, '')).encode('utf-8').strip()

	def is_user_registered(self, user):
		"""Return true if the given user has an **active**
		registration for this competition, else return false"""
		if user.is_anonymous():
			return False
		return self.registration_set.filter(user=user.pk, active=True).exists()
