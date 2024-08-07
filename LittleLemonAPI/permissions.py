from rest_framework import permissions


class ManagerPermission(permissions.BasePermission):
    """
    Has manager permissions if the request.user is apart of the manager group
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()