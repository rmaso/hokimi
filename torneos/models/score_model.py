from django.db import models
from django.contrib.auth.models import User

from .torneo_model import Torneo

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'scores/user_{0}/{1}/{2}'.format(instance.user_id, instance.competition_id, filename)

class Score(models.Model):
    class Meta:
        app_label = 'torneos'

    s_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True)
    competition = models.ForeignKey(Torneo, null=True, blank=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(blank=True, max_length=255)
    document = models.FileField(upload_to=user_directory_path)
    score = models.FloatField(null=True, blank=True)
    error = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
#        fields = [(f.verbose_name, f.name) for f in Score._meta.get_fields()]
        return ', '.join(Score._meta.get_all_field_names())

