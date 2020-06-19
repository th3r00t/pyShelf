from base64 import b64encode

from django import template

register = template.Library()


@register.filter(name='bin_2_img')
def bin_2_img(_bin):
    if _bin is not None:
        return b64encode(_bin).decode("utf-8")
    else: return None


@register.simple_tag(name='make_description_obj')
def make_description_obj(description):
    if description is not None:
        return description[0:225]+"..."
    else: return None
