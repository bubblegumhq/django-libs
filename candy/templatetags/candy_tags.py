# -*- coding: utf-8 -*-
import json
import locale
from django.core.serializers import serialize
from django.db.models import QuerySet

from django.template import Library


# MAKE SURE
#
# TEMPLATE_CONTEXT_PROCESSORS has "django.core.context_processors.request",
from django.utils.safestring import mark_safe

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
    return json.dumps(obj)

def jsonify(object):
    return json.dumps(object)
register.filter('jsonify', jsonify)

def jsonify_qs(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(serialize('json', [object]))
register.filter('jsonify_qs', jsonify_qs)

def resize_image(url, size):
    if "filepicker" in url:
        width, height = size.split("x")
        return url + "/convert?width=%s&height=%s&fit=crop" % (width, height)
    return url
register.filter('resize_image', resize_image)

