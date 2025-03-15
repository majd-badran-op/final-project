class BookNotFoundError(Exception):
    def __init__(self, message='Book not found'):
        self.message = message
        super().__init__(self.message)


class BookAlreadyBorrowedError(Exception):
    def __init__(self, message='Book is already borrowed'):
        self.message = message
        super().__init__(self.message)


class FailedToDeleteBookError(Exception):
    def __init__(self, message='Failed to delete book'):
        self.message = message
        super().__init__(self.message)


class BookReturnError(Exception):
    def __init__(self, message='Book is already not borrowed'):
        self.message = message
        super().__init__(self.message)
