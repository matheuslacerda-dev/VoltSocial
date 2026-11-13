class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} was not found.")


class UserAlreadyExistsError(Exception):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"User {field} is already in use.")
