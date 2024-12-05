from django import template

register = template.Library()


@register.filter
def split_text_by_length(value, length):
    if not isinstance(value, str) or length < 1:
        return value
    segments = [value[i : i + length] for i in range(0, len(value), length)]
    return "<br>".join(segments)
