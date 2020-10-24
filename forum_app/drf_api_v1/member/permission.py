from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from forum_app.models import Member

class IsOwner(BasePermission):
    message = _("You must be the owner to do this.")

    def has_object_permission(self, request, view, obj):
        return obj == request.user
    
class IsAdmin(BasePermission):
    message = _("You must be Admin to do this.")
    
    def has_permission(self, request, view):
        member = Member.objects.get(user=request.user)
        return member.types == Member.ADMIN
