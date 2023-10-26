from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight_text(text, search):
    text = text.replace('ё', 'е')
    for s in search:
        try:
            s = s.replace('ё', 'е')
            word_pattern = '(\s)+'.join(['[,|!|?|;|:|.|-|—]*(/s)*(/t)*'+i+'(/s)*(/t)*[,|!|?|;|:|.|-|—]*' for i in s.split()])
            pattern = re.compile(word_pattern)
            matches = list(pattern.search(text.lower()).span())
            text = list(text)
            text[matches[0]] = '<span style="background-color: #f9ffb7; font-weight: bold; font-style: italic;">'+text[matches[0]]
            text[matches[1]-1] = text[matches[1]-1]+'</span>'
            text = ''.join(text)
        except:
            continue
    return mark_safe(text)

@register.filter
def unique_words(res):
    unique = []
    for sent in res[0]:
        for w in sent[0]:
            if w not in unique:
                unique.append(w)
    return unique
