from enum import StrEnum

from app.models.enums import UserRole


class Permission(StrEnum):
    POST_CREATE = "post:create"
    POST_PUBLISH = "post:publish"
    POST_EDIT_ANY = "post:edit_any"
    POST_DELETE_ANY = "post:delete_any"
    COMMENT_CREATE = "comment:create"
    COMMENT_MODERATE = "comment:moderate"
    USER_MANAGE = "user:manage"


_USER = frozenset({Permission.COMMENT_CREATE})
_AUTHOR = _USER | {Permission.POST_CREATE, Permission.POST_PUBLISH}
_MODERATOR = _AUTHOR | {
    Permission.COMMENT_MODERATE,
    Permission.POST_DELETE_ANY,
    Permission.POST_EDIT_ANY,
}
_ADMIN = frozenset(Permission)


ROLE_PERMISSIONS: dict[UserRole, frozenset[Permission]] = {
    UserRole.USER: _USER,
    UserRole.AUTHOR: _AUTHOR,
    UserRole.MODERATOR: _MODERATOR,
    UserRole.ADMIN: _ADMIN,
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, frozenset())
