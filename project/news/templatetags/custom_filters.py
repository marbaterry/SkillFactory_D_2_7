from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str

