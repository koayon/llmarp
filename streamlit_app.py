import openai
import streamlit as st

# Set the sentence in memory but not displayed
sentence = "The quick brown fox jumps over the lazy dog"
# Split the sentence into words
words = sentence.split(" ")

# Create an uneditable textbox at the top
st.text(
    "Correct words will be shown here with green underline. Incorrect words will be shown with red strikethrough along with correct word."
)

if "word_index" not in st.session_state:
    st.session_state["word_index"] = 0
    st.session_state["all_words"] = []
    st.session_state["user_score"] = 0

user_word = ""


def submit_word():
    # If user_word contains enter key, submit the word
    global _user_word
    global user_word
    if _user_word[-1] == "\n":
        user_word = _user_word[:-1].strip()
        _user_word = ""


_user_word = st.text_input(
    label="Enter a word",
    on_change=submit_word()
    # key=f"word_input_{st.session_state.word_index}"
)


def update_textbox(word, correct_word, is_correct):
    if is_correct:
        return f'<u style="color: green">{word}</u>'
    else:
        return f'<del style="color: red">{word}</del> {correct_word}'


def prompt_ai(start_of_sentence):
    # TODO: Write prompt
    raise NotImplementedError


def tokenize_sentence(sentence):
    raise NotImplementedError


def reset_game():
    st.session_state["word_index"] = 0
    st.session_state["all_words"] = []
    st.session_state["user_score"] = 0
    sentence = get_new_sentence()


def get_new_sentence():
    raise NotImplementedError


reset_button = st.button("Reset game")
if reset_button:
    # reset_game()
    raise NotImplementedError


# Check if the form is submitted
if user_word:
    word_index = st.session_state["word_index"]
    is_word_correct = user_word == words[word_index]

    # ai_word = prompt_ai(words[:word_index])
    # is_ai_correct = ai_word == words[word_index]

    st.session_state.all_words.append(
        update_textbox(user_word, words[word_index], is_word_correct)
    )
    st.session_state["word_index"] += 1
    st.session_state["user_score"] += 1 if is_word_correct else 0


st.write(st.session_state["word_index"])

if user_word:
    st.write(
        "User score",
        st.session_state.user_score,
        "out of ",
        st.session_state.word_index,
    )

st.markdown(" ".join(st.session_state.all_words), unsafe_allow_html=True)
