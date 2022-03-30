from django import template

register = template.Library()

BAD_WORDS = ['мать','твою','тудыть']

@register.filter(name='Censor')
def Censor(value):
    for word in BAD_WORDS:
        value = value.replace(word[0:], '*' * (len(word) - 1))

    return value