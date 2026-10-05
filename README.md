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

### Game purpose

Glitchy Guesser is a number guessing game built with Streamlit. The game picks a secret number in a range set by the difficulty (Easy 1–20, Normal 1–100, Hard 1–50). The player has a limited number of attempts to guess it. After each guess, the game gives a hint (go higher or go lower) and updates the score. The game ends when the player guesses correctly or runs out of attempts. The New Game button is supposed to start a fresh round.

### Bugs found

I reviewed `app.py` and `logic_utils.py` with Claude. These were the main bugs:

1. **The hints were backwards.** A guess above the secret said "Go HIGHER", and a guess below said "Go LOWER". *(Fixed)*
2. **New Game didn't clear the history.** Guesses from the previous game stayed in the history. *(Fixed)*
3. **You couldn't play again after a game ended.** New Game didn't reset the status from "won" or "lost", so the app kept showing "Game over". *(Fixed)*
4. **Every second guess compared the numbers as text.** On even attempts the secret became a string, so `9` vs `"50"` was compared character by character and gave a wrong hint. *(Not fixed)*
5. **The attempt count was off by one.** Attempts started at 1 but New Game reset them to 0, so the first game gave one fewer guess. *(Not fixed)*
6. **New Game ignored the difficulty.** It always picked a secret from 1–100, and changing difficulty didn't pick a new secret. *(Not fixed)*
7. **The scoring was inconsistent.** A wrong "Too High" guess could add points, and the win formula took off an extra 10 points. *(Not fixed)*
8. **Smaller issues.** The prompt always said "1 and 100", invalid input used up an attempt, decimals were silently cut down, and New Game didn't reset the score. *(Not fixed)*

### Fixes applied

- **Hints:** swapped the "Go HIGHER" and "Go LOWER" messages in `check_guess`, in both the normal branch and the `except TypeError` branch.
- **History:** added `st.session_state.history = []` to the New Game block in `app.py`.
- **Game status:** added `st.session_state.status = "playing"` to the New Game block, so a new game can start after a win or loss.
- **Refactor:** moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` from `app.py` into `logic_utils.py`, and changed `app.py` to import them. I kept `check_guess` returning `(outcome, message)` and updated the three original tests to match.
- **Tests:** added pytest tests in `tests/test_game_logic.py` for each fix. They use Streamlit's `AppTest` to submit guesses and click New Game. All 7 tests pass (see Test Results below).

Each fix in the code has a `# FIXME` comment describing the bug and a `# FIX` comment describing how I worked with AI on it.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- User enters a guess of a number -->
2. <!-- If number in guess is > that the number in the secret, Game returns too high -->
3. <!-- If number in guess is < that the number in the secret, Game returns too low -->
4. <!-- Score is begin updated after each guess -->
5. <!-- A correct answer ends the game with a display of emojia and score -->
6. <!-- Strat a game clears and reset the attemt count, history ans score -->
7. <!-- Game level can be selected but current set to Normal (1 - 100) -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================

(.venv) PS C:\Users\johnp\CodePath\AI110\ai110-module1show-gameglitchinvestigator-starter> python -m pytest tests/test_game_logic.py -v
==================================== test session starts =====================================
platform win32 -- Python 3.13.16, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\johnp\CodePath\AI110\ai110-module1show-gameglitchinvestigator-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\johnp\CodePath\AI110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 7 items                                                                             

tests/test_game_logic.py::test_winning_guess PASSED                                   [ 14%]
tests/test_game_logic.py::test_guess_too_high PASSED                                  [ 28%]
tests/test_game_logic.py::test_guess_too_low PASSED                                   [ 42%]
tests/test_game_logic.py::test_too_high_guess_says_go_lower PASSED                    [ 57%]
tests/test_game_logic.py::test_too_low_guess_says_go_higher PASSED                    [ 71%]
tests/test_game_logic.py::test_new_game_clears_history PASSED                         [ 85%]
tests/test_game_logic.py::test_new_game_after_loss_lets_you_play_again PASSED         [100%]

=================================== 7 passed in 3.67s ======================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
