from django import template

#建立模板对象
register = template.Library()

@register.filter(name='sub1')
def whatever(value):
    return value-1