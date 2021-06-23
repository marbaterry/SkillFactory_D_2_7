from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    obscene_values = [
        'word1', 'word2', 'word3', 'title_number_4'
    ]
    if isinstance(value, str):
        for i in value.split():
            if i in obscene_values:
                value = value.replace(i, '***')
    return value


@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')
