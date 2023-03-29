from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Удалять или редактировать может только автор,
    запрос get список всех публикаций или отдельную публикацию
    может любой пользователь.
    Создавать новую публикацию может только аутентифицированный пользователь.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всех публикаций
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем только авторам редактировать или удалять свои публикации
        return obj.author == request.user
