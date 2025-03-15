class MemberNotFoundError(Exception):
    def __init__(self, message='Member not found'):
        self.message = message
        super().__init__(self.message)


class FailedToAddMemberError(Exception):
    def __init__(self, message='Failed to add member'):
        self.message = message
        super().__init__(self.message)


class FailedToDeleteMemberError(Exception):
    def __init__(self, message='Failed to delete member'):
        self.message = message
        super().__init__(self.message)


class MemberBooksNotFoundError(Exception):
    def __init__(self, message='Member doesn\'t have any books'):
        self.message = message
        super().__init__(self.message)
