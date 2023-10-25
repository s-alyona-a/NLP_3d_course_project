from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight_text(text, search):
    for i in search:
        highlighted = re.sub(r'\b'+i+r'\b', '<span style="background-color: #f9ffb7; font-weight: bold; font-style: italic;">{}</span>'.format(i), text, flags=re.IGNORECASE)
        text = highlighted
    return mark_safe(text)

@register.filter
def unique_words(res):
    unique = []
    for sent in res[0]:
        for w in sent[0]:
            if w not in unique:
                unique.append(w)
    return unique