class BaseUser:
    """
        Is the base of all the users in the game
    """
    def __init__(self, user_id: str, name: str, role: str):
        self.name = name
        self.role = role
        self.user_id = user_id
