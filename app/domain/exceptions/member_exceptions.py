class MemberNotFoundError(Exception):
    def __init__(self, message: str = 'Member not found') -> None:
        self.message = message
        super().__init__(self.message)


class FailedToAddMemberError(Exception):
    def __init__(self, message: str = 'Failed to add member') -> None:
        self.message = message
        super().__init__(self.message)


class FailedToDeleteMemberError(Exception):
    def __init__(self, message: str = 'Failed to delete member') -> None:
        self.message = message
        super().__init__(self.message)


class MemberBooksNotFoundError(Exception):
    def __init__(self, message: str = 'Member doesn\'t have any books') -> None:
        self.message = message
        super().__init__(self.message)


class EmailAlreadyExistsError(Exception):
    def __init__(self, message: str = 'The email address already exists.') -> None:
        self.message = message
        super().__init__(self.message)
