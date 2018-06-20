from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def dae_export_url(model):
    meta = model._meta
    return reverse('dae_export', args=(meta.app_label, meta.object_name))
