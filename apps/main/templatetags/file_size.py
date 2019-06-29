from django import template

register = template.Library()


@register.filter
def file_size(value):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|file_size }}
    """
    value = int(value)
    if value < 512000:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'mb'
    else:
        value = value / 1073741824.0
        ext = 'gb'
    return '%s %s' % (str(round(value, 2)), ext)
