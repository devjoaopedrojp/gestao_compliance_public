from django import template
import re

register = template.Library()


@register.filter
def highlight(text, search):
    if search:
        escaped_search = re.escape(search)
        return re.sub(
            f"({escaped_search})",
            r'<span class="highlight">\1</span>',
            text,
            flags=re.IGNORECASE,
        )
    return text
