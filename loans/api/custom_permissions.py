from rest_framework import permissions


class IsLenderOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow wallet users/owners of an object
    to access the wallet. Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `user`.
        return obj.user == request.user


class IsBorrowerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow wallet users/owners of an object
    to access the wallet. Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `user`.
        return obj.user == request.user


class IsLoanBorrowerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow wallet users/owners of an object
    to access the wallet. Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `user`.
        return obj.borrower == request.user.borrower
