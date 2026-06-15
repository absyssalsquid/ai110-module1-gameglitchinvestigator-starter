import re

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100

def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """

    raw = raw.strip() if raw else ""

    if not raw:
        return False, None, "Enter a guess."
    
    # reject negative and non integer values outright instead of truncating floats, which users may not expect
    # provide more explicit guidance on the types of inputs accepted
    if re.search(r'[^0-9]', raw):
        return False, None, "Enter a positive integer." 
    
    if len(raw) > 20:
        return False, None, "Number is too large."

    value = int(raw)
    if value == 0:
        return False, value, "Enter a positive, non-zero integer." 

    return True, value, None

def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    elif guess > secret:
        return "Too High", "📉 Go LOWER!" # FIXED: used claude planning mode to fix hint error
    else:
        return "Too Low", "📈 Go HIGHER!"
        
    # REMOVED: parse_guess ensures that the guess is always an int and the secret is now always passed as an int
    # except TypeError:
    #     g = str(guess)
    #     if g == secret:
    #         return "Win", "🎉 Correct!"
    #     if g > secret:
    #         return "Too High", "📈 Go HIGHER!"
    #     return "Too Low", "📉 Go LOWER!"

def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        points = max(points, 10) 

    elif outcome == "Too High":
        points = -5 if attempt_number % 2 == 1 else 5 

    elif outcome == "Too Low":
        points = -5

    return current_score + points