from django import template

register = template.Library()


@register.filter(name='active')
def is_active(things):
    return things.filter(active=True)
