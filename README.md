# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. The game starts. A secret random number is generated for the user to determine within a limited number of tries. The range and number of allowed guesses depends on the selected difficulty.
2. The user enters a strictly numeric guess, fewer than 20 digits. If not, the user receives an error message.
3. The user receives a hint if the guess is too low ("go higher") or too high ("go lower"). If the guess is correct, the round ends.
4. The user submits guesses until the guess is correct or they run out of attempts. If correct, a congratulatory message is displayed with a balloon effect. If out of tries, a failure message is shown.
5. The game does not accept guesses at this point. If the user tries, a message instructs them to start a new game.
6. The user starts a new round and begins again.
7. At any point, the user can change the game difficulty. This affects the generated number range and number of allowed guesses. Upon selecting a new difficulty, a new round is started.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
tests/test_game_logic.py::test_winning_guess PASSED                         [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                        [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                         [ 21%]
tests/test_game_logic.py::test_parse_empty PASSED                           [ 28%]
tests/test_game_logic.py::test_parse_valid_numbers PASSED                   [ 35%]
tests/test_game_logic.py::test_parse_whitespace PASSED                      [ 42%]
tests/test_game_logic.py::test_parse_special_float PASSED                   [ 50%]
tests/test_game_logic.py::test_parse_alphanumeric_strings PASSED            [ 57%]
tests/test_game_logic.py::test_parse_special_characters PASSED              [ 64%]
tests/test_game_logic.py::test_parse_zero PASSED                            [ 71%]
tests/test_game_logic.py::test_parse_negative PASSED                        [ 78%]
tests/test_game_logic.py::test_parse_decimals PASSED                        [ 85%]
tests/test_game_logic.py::test_parse_big_numbers PASSED                     [ 92%]
tests/test_game_logic.py::test_difficulty_range PASSED                      [100%]

=============================== 14 passed in 0.03s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
