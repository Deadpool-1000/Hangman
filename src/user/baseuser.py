class BaseUser:
    """
        Is the base of all the users in the game
    """
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
