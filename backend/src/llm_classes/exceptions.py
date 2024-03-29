class RoleException(Exception):
    '''
    Raised when choosing multiple roles.
    '''
    def __init__(self):
        self.message = "Cannot be both assistant and llm!"
        super().__init__(self.message)

class EmptyException(Exception):
    '''
    Raised when a ChatLog is instantiated with an empty list.
    '''
    def __init__(self):
        self.message = "Cannot have empty message list!"
        super().__init__(self.message)