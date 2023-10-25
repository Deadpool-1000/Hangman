class HangmanPrompts:
    MAIN_PROMPT = """
Hey, Welcome to Hangman Press:
'l' : login
's' : signup
'q' : quit
Your Choice: """
    ADMIN_PROMPT = """
'l': leaderboard section
'w' : word list section
'p' : New Game
'q' : logout
Your Choice: """
    PLAYER_PROMPT = """
Press:
'p': For a new game
'l': leaderboard
'q': logout
Your choice: """
    MODIFY_GAME_PROMPT = """
What do you want to modify?
'r': number of rounds
'd': difficulty levels
'b': back """
    SECURE_PASSWORD_PROMPT = """
Your password must contain:
1. Minimum eight characters, 
2. at least one uppercase letter
3. one lowercase letter and one number
New Password: """
