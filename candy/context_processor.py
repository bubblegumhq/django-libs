from django.conf import settings
from django.contrib.sites.models import Site


def candy_context(request):
    return {
        'SETTINGS': settings,
        'SITE': Site.objects.get_current(),
    }

