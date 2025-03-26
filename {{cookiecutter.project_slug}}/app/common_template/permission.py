from rest_framework import permissions
from rest_framework.authtoken.models import Token
from services.dynamo import is_user_a_part_of_business


class BusinessMatchesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        business_id = request.business_id
        if not business_id:
            return False

        if not request.user.is_authenticated:
            return False

        if not is_user_a_part_of_business(request.user.id, business_id):
            # If the user has a Token object set then it is an "API" user in
            # Django's DB (i.e. is another Marky system) and is allowed to act on
            # behalf of all businesses therefore we let the request through.
            return Token.objects.filter(user=request.user).exists()

        return True
