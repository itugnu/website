from django import template

register = template.Library()


@register.filter
def dictindex(obj, index):
    """Get dictionary item using index.
    Usage: {{ object|dictindex:index }}
    :param obj: Object to get index from
    :param index: int or str index of object
    """
    return obj[index]
