from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class UserRole(StrEnum):
    USER = "user"
    AUTHOR = "author"
    MODERATOR = "moderator"
    ADMIN = "admin"
