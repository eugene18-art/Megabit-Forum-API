from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
import re

User = get_user_model()

def generate_username(first_name,last_name):
    val = "{0}{1}".format(first_name,last_name).lower().replace(" ", "")
    if User.objects.filter(username=val).count() == 0:
        return val
    qs = User.objects.filter(username__regex=rf"^{val}\d+").order_by("-username")
    counters = [int(re.search(r"\d+$", str(x)).group(0)) for x in qs]
    if len(counters) == 0:
        return f"{val}{0}"
    counters.sort()
    max_counter = counters.pop()
    max_counter+=1
    val = f"{val}{max_counter}"
    return val

def get_user_or_404(username):
    try:
        query_user = User.objects.get(username=username)
        return query_user
    except (User.DoesNotExist):
        raise exceptions.NotFound(detail=_("The resource you're looking for does not exists."))