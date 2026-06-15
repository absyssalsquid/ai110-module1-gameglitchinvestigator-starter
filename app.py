import random
import streamlit as st

from logic_utils import * 


# =======================================================

DEFAULT_STATE_VARS = {
    "attempts": 0, # FIXED: was being initialized as 1
    "score": 0,
    "status": "playing",
    "history": [],
    "difficulty": "Normal", # later overwritten by selectbox, but needed here to determine initial range and secret number
    "reset_game": False # FIXED: allows new game logic to be shared by button and selecting new difficulty
}
for key, default_value in DEFAULT_STATE_VARS.items():
    st.session_state.setdefault(key, default_value)

low, high = get_range_for_difficulty(st.session_state.difficulty)
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[st.session_state.difficulty]

# hide "[press enter to apply", as it is somewhat confusing
st.html(
    """
    <style>
    div[data-testid="InputInstructions"] {
        visibility: hidden;
    }
    </style>
    """
)

# =======================================================

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
    key="difficulty", # FIXED: added key to selectbox to store selected difficulty in session state
    on_change=lambda: st.session_state.update({"reset_game": True})  # FIXED: allows new game logic to be shared by button and selecting new difficulty
)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")

info_placeholder = st.empty()
debug_expander = st.expander("Developer Debug Info") # FIXED: moved populating the expander to the end so it shows latest state. claude's suggested fix for rerun caused other problems, but the explanation of render order helped me realize how to fix

raw_guess = st.text_input(
    "Enter your guess:"
    # key=f"guess_input_{difficulty}" # REMOVED: key not used in code
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁", on_click=lambda: st.session_state.update({"reset_game": True})) # FIXED: allows new game logic to be shared by button and selecting new difficulty
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.session_state.reset_game == True:
    st.session_state.reset_game = False
    st.session_state.status = "playing" # FIXED: reset status to playing when new game starts, otherwise user can't play again after winning or losing once
    st.session_state.attempts = 0
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    st.session_state.secret = random.randint(low, high) # FIXED: new secret number generated based on current difficulty range, auto suggested by copilot
    st.success("New game started.")
    print("new game started")

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # MOVED: increment attempt only if input is ok, instead of after every submit
        st.session_state.attempts += 1

        # FIXED: noticed when looking at check_guess logic. removed because there's no reason for the secret to alternate between being parsed a string and an int
        # if st.session_state.attempts % 2 == 0:
        #     secret = str(st.session_state.secret)
        # else:
        #     secret = st.session_state.secret

        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

info_placeholder.info( # FIXED: moved to end to show latest info
    f"Guess a number between {low} and {high}. " # FIXED: updated to show correct range based on difficulty, auto suggested by copilot
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with debug_expander:
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", st.session_state.difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
