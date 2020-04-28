
from django import template
from apps.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindSubUser(user_value, plan_id):
    try:
        subscription.objects.get(user = user_value, plan = plan.objects.get(id = plan_id))
        return True
    except:
        return False

register.filter(FindSubUser)