import streamlit as st
import random

PROTOTYPE = """
 ┏━━━┑
 ┃   O>
 ┃ >╦╧╦<
 ┃  ╠═╣
 ┃  ╨ ╨
 ┻━━━━━━
"""

STEPS = [
"""
 ┏━━━┑
 ┃
 ┃
 ┃
 ┃
 ┻━━━━━━
""",
"""
 ┏━━━┑
 ┃   O
 ┃
 ┃
 ┃
 ┻━━━━━━━
""",
"""
 ┏━━━┑
 ┃   O>
 ┃
 ┃
 ┃
 ┻━━━━━━
""",
"""
 ┏━━━┑
 ┃   O>
 ┃  ╔╧╗
 ┃  ╚═╝
 ┃
 ┻━━━━━━
""",
"""
 ┏━━━┑
 ┃   O>
 ┃ >╦╧╗
 ┃  ╚═╝
 ┃
 ┻━━━━━━
""",
"""
 ┏━━━┑
 ┃   O>
 ┃ >╦╧╦<
 ┃  ╚═╝
 ┃
 ┻━━━━━━
""",
"""
 ┏━━━┑
 ┃   O>
 ┃ >╦╧╦<
 ┃  ╠═╝
 ┃  ╨
 ┻━━━━━━
""",
"""
 ┏━━━┑
 ┃   O>
 ┃ >╦╧╦<
 ┃  ╠═╣
 ┃  ╨ ╨
 ┻━━━━━━
"""
]

def get_word():
    MIN_LENGTH = 3
    MAX_LENGTH = 8
    with open('assets/words1000.txt') as f:
        words = [line.strip() for line in f]
    words = [w for w in words if MIN_LENGTH <= len(w) <= MAX_LENGTH]
    word = random.choice(words)
    return word

def show():
    st.text(STEPS[st.session_state.step])
    chars = [c if c in st.session_state.guessed else "_" for c in st.session_state.word]
    st.text(" "+" ".join(chars))
    st.text("guessed: "+" ".join(st.session_state.guessed))

def process(c):
    if c < 'a' or c > 'z':
        st.error("Must be a lowercase letter!")
    elif c in st.session_state.guessed:
        st.warning("You already guessed that one!")
    else:
        st.session_state.guessed.append(c)
        if c not in st.session_state.word:
            st.session_state.step += 1
            if st.session_state.step == len(STEPS) - 1:
                st.error("YOU LOSE, the word was "+st.session_state.word)
                st.session_state.can_play = False
        elif all(c in st.session_state.guessed for c in st.session_state.word):
            st.success("YOU WIN!!")
            st.balloons()
    show()

if "can_play" not in st.session_state:
    st.session_state.can_play = True
if "step" not in st.session_state:
    st.session_state.step = 0
if "guessed" not in st.session_state:
    st.session_state.guessed = []
if "word" not in st.session_state:
    st.session_state.word = get_word()

st.title("Hang Chicken")

c1, c2, c3 = st.columns([1,2,3])
c1.markdown("")
c1.markdown("")
if c1.button("New Game"):
    st.session_state.step = 0
    st.session_state.guessed = []
    st.session_state.word = get_word()
    st.session_state.can_play = True

if st.session_state.can_play:
    c = c2.text_input("pick a letter: ", max_chars=1).lower()
    process(c)
