from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MyApphook(CMSApp):
    name = _("torneos")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["torneos.urls"]       # replace this with the path to your application's URLs module

apphook_pool.register(MyApphook)