class BookNotFoundError(Exception):
    def __init__(self, message: str = 'Book not found') -> None:
        self.message = message
        super().__init__(self.message)


class BookAlreadyBorrowedError(Exception):
    def __init__(self, message: str = 'Book is already borrowed') -> None:
        self.message = message
        super().__init__(self.message)


class FailedToDeleteBookError(Exception):
    def __init__(self, message: str = 'Failed to delete book') -> None:
        self.message = message
        super().__init__(self.message)


class BookReturnError(Exception):
    def __init__(self, message: str = 'Book is already not borrowed') -> None:
        self.message = message
        super().__init__(self.message)
