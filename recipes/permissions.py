from rest_framework import permissions


class IsRecipeAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user


class IsRecipeComponentAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.recipe.author.user == request.user


class IsRecipePublished(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.published


class IsRecipeComponentPublished(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.recipe.published