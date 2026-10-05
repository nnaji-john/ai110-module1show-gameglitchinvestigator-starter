# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 80| | | go higher         | go lower | in app.py
| history| reset in a game restart| append  a new row += | in app.py
| 28| | | go lower          | go higer | in app.py

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**Tools:** I used Claude (Claude Code in VS Code, in agent mode). I first asked it to review `app.py` and `logic_utils.py` without changing anything. Then I had it make specific fixes, write pytest tests, and refactor the logic into `logic_utils.py`.

**A suggestion that was correct:** I noticed the hints were backwards, and Claude confirmed it. In `check_guess`, a guess above the secret returned "Go HIGHER" and a guess below returned "Go LOWER", and the same swap appeared again in the `except TypeError` branch. Claude swapped the messages in both places and wrote pytest tests that set the secret to 50, guess 60 and 40, and check that the hint says "Go LOWER" and "Go HIGHER". I verified the fix by running `python -m pytest tests/test_game_logic.py -v` myself and seeing the tests pass. Claude also showed that the tests fail when the old swapped messages are put back, so they really do catch this bug.

**A suggestion I did not accept as written:** When refactoring, Claude pointed out that the original tests expected `check_guess` to return only the outcome (like `"Too High"`), while the app's version returns a pair (`"Too High", "Go LOWER!"`). It offered to change `check_guess` to return only the outcome and have `app.py` look up the message separately. I rejected that and chose to keep the pair and update the three original tests instead, because [fill in your reason, e.g. it kept `app.py` working the way it already did and meant fewer changes]. To verify, I ran the full test suite, and all the tests, original and new, passed with the updated tests (`outcome, _ = check_guess(60, 50)`).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
