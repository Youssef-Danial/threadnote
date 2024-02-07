from django import template
from home.models import User, Access, Note, Thread
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.simple_tag(name="rena")
def rena(oner, name):
    access_type_options = {
        "v" : "Access View",
        "e" : "Access Edit"
    }
    return access_type_options[name]

@register.simple_tag
def is_authorized(user_id, thread_id):
    user = get_object_or_404(User, id=user_id)
    thread = get_object_or_404(Thread, id=thread_id)
    if user in thread.users.all() or user == thread.creator:
        return True
    else:
        return False

@register.simple_tag
def is_authorized_edit(user_id, thread_id):
    user = get_object_or_404(User, id=user_id)
    thread = get_object_or_404(Thread, id=thread_id)
    access = Access.objects.filter(thread= thread, user=user).first()
    if user == thread.creator or access.access_type == "e":
        return True
    else:
        return False

@register.filter
@stringfilter
def accesstype(name):
    access_type_options = {
        "v" : "Access View",
        "e" : "Access Edit"
    }
    return access_type_options[name]