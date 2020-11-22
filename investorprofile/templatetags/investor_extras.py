from django import template

register = template.Library()

@register.filter(name='zip')
def zip_lists(batch, user_stocks):
    return zip(batch, user_stocks)
