# -*- coding: utf-8 -*-
import json
import locale

from django.template import Library


# MAKE SURE
#
# TEMPLATE_CONTEXT_PROCESSORS has "django.core.context_processors.request",
register = Library()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# MAKE SURE
#
# TEMPLATE_CONTEXT_PROCESSORS has "django.core.context_processors.request",

@register.simple_tag
def active(request, pattern):
    import re

    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.simple_tag
def as_json(obj):
    return json.dumps(obj, indent=2)
