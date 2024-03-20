from django import template


register = template.Library()

BADWORDS = ("тренером", "цены", "политику")

@register.filter()
def censor(text):
    new_content = text
    for i in BADWORDS:
        new_content = new_content.replace(i, i[:1]+'*'*(len(i)-1))
    return new_content