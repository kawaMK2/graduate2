from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnAccountOrReadOnly(BasePermission):
    """
    Note:
        Custom permissionについて   http://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
        メソッドがreadonlyか操作対象userがリクエストしたuserと同一なら許可
    """
    message = 'You must login to own account.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
