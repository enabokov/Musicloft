import os
from django import template

register = template.Library()


@register.filter
def check(path):
    path = path.split('/')

    absolute_path, relative_path = path, path[1:].copy()
    absolute_path[0] = 'static'
    absolute_path = os.path.join('music', *absolute_path)
    if not len(relative_path):
        return absolute_path

    relative_path = os.path.join(*relative_path)
    return relative_path if os.path.exists(absolute_path) else None
