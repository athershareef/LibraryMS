from django import template

register = template.Library()


@register.simple_tag
def get(a, b):
    if not a:
        return b[0]
    li = a[b[0]]
    return int(li[0])


@register.simple_tag
def getb(a, b):
    li = a[b[2]]
    return int(li[0])


@register.simple_tag
def getp(a):
    li = a.split(",")
    return int(li[0])
