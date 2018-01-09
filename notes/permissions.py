from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Note:
        Custom permissionについて   http://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
        メソッドがreadonlyか操作対象objに関連づけられたuserがリクエストしたuserと同一なら許可
    """
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

