from logic_utils import check_guess, parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, msg = check_guess(50, 50)
    assert result == "Win"
    assert msg == "🎉 Correct!"
 
def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, msg = check_guess(60, 50)
    assert result == "Too High"
    assert msg == "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, msg = check_guess(40, 50)
    assert result == "Too Low"
    assert msg == "📈 Go HIGHER!"

def test_parse_empty():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("   ") == (False, None, "Enter a guess.")
    assert parse_guess(None) == (False, None, "Enter a guess.")

def test_parse_valid_numbers():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("38") == (True, 38, None)
    
def test_parse_whitespace():
    assert parse_guess("  7") == (True, 7, None)
    assert parse_guess("7  ") == (True, 7, None)
    assert parse_guess("\t7\n") == (True, 7, None)

def test_parse_special_float():
    assert parse_guess("nan") == (False, None, "Enter a positive integer.")
    assert parse_guess("NaN") == (False, None, "Enter a positive integer.")
    assert parse_guess("inf") == (False, None, "Enter a positive integer.")
    assert parse_guess("-inf") == (False, None, "Enter a positive integer.")

def test_parse_alphanumeric_strings():
    assert parse_guess("abc") == (False, None, "Enter a positive integer." )
    assert parse_guess("12abc") == (False, None, "Enter a positive integer." )
    assert parse_guess("one") == (False, None, "Enter a positive integer." )

def test_parse_special_characters():
    assert parse_guess("!@#") == (False, None, "Enter a positive integer." )
    assert parse_guess("$5") == (False, None, "Enter a positive integer." )
    # underscores are not valid in numbers, even though python allows them. ensure only simple numeric input.
    assert parse_guess("1_000") == (False, None, "Enter a positive integer.")

def test_parse_zero():
    assert parse_guess("0") == (False, 0, "Enter a positive, non-zero integer.")
    assert parse_guess("0"*20) == (False, 0, "Enter a positive, non-zero integer.")

def test_parse_negative():
    assert parse_guess("-1") == (False, None, "Enter a positive integer.")
    assert parse_guess("-999") == (False, None, "Enter a positive integer.")

def test_parse_decimals():
    assert parse_guess("3.14") == (False, None, "Enter a positive integer." )
    assert parse_guess("9.99") == (False, None, "Enter a positive integer." )
    assert parse_guess("5.") == (False, None, "Enter a positive integer." )
    assert parse_guess(".5") == (False, None, "Enter a positive integer." )

def test_parse_big_numbers():
    assert parse_guess("9"*21) == (False, None, "Number is too large.")
    assert parse_guess("9" * 20) == (True, int("9" * 20), None)
    assert parse_guess(" " + "9" * 20) == (True, int("9" * 20), None)

def test_difficulty_range():
    assert get_range_for_difficulty("Easy") == (1,20)
    assert get_range_for_difficulty("Normal") == (1,100)
    assert get_range_for_difficulty("Hard") == (1,50)