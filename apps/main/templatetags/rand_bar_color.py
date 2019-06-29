from random import randint
from django.template import Library
register = Library()


@register.assignment_tag()
def random_color():

    colors = ['aba500', 'ec0027', '88aa00', '00881a']

    return colors[randint(0, 3)]
