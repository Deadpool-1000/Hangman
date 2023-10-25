
def menu(prompt: str, allowed: list[str]) -> str:
    """
    generator for menu that renders menu prompt provide repetitively and provides some basic input validation
    :yield str (user choice: a single character)
    """
    user_choice = input(prompt)
    while user_choice != 'q':
        if user_choice not in allowed:
            while user_choice not in allowed and user_choice != 'q':
                user_choice = input("Enter valid input: ")
            if user_choice == 'q':
                continue
        yield user_choice
        user_choice = input(prompt)



