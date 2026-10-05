from streamlit.testing.v1 import AppTest

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def _submit_guess(at, guess):
    at.text_input(key="guess_input_Normal").input(guess)
    at.button[0].click()  # "Submit Guess 🚀"
    return at.run()


def test_too_high_guess_says_go_lower():
    # Bug: a guess above the secret used to say "Go HIGHER"
    at = AppTest.from_file("../app.py")
    at.session_state["secret"] = 50
    at.run()

    at = _submit_guess(at, "60")

    assert at.warning[0].value == "Go LOWER!"


def test_too_low_guess_says_go_higher():
    # Bug: a guess below the secret used to say "Go LOWER"
    at = AppTest.from_file("../app.py")
    at.session_state["secret"] = 50
    at.run()

    at = _submit_guess(at, "40")

    assert at.warning[0].value == "Go HIGHER!"


def test_new_game_clears_history():
    # Bug: clicking "New Game" left the previous game's guesses in history
    at = AppTest.from_file("../app.py")
    at.session_state["secret"] = 50
    at.run()

    at = _submit_guess(at, "40")
    assert at.session_state["history"] == [40]

    at.button[1].click()  # "New Game 🔁"
    at.run()

    assert at.session_state["history"] == []


def test_new_game_after_loss_lets_you_play_again():
    # Bug: after losing, "New Game" left status as "lost", so the game stayed stuck on "Game over"
    at = AppTest.from_file("../app.py")
    at.session_state["secret"] = 50
    at.session_state["attempts"] = 7  # one guess left on Normal
    at.run()

    at = _submit_guess(at, "40")
    assert at.session_state["status"] == "lost"

    at.button[1].click()  # "New Game 🔁"
    at.run()

    assert at.session_state["status"] == "playing"
    assert len(at.error) == 0
