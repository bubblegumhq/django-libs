from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'jawache'


def LoginRequiredDecorator(ClassView):
    ClassView.dispatch = method_decorator(login_required)(ClassView.dispatch)
    return ClassView