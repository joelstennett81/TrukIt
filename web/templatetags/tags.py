# myapp/templatetags/user_tags.py

from django import template
from api.models import *

register = template.Library()


@register.simple_tag
def user_is_admin(user):
    return user.is_staff
