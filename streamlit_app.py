import streamlit as st

# Set the sentence in memory but not displayed
sentence = "The quick brown fox jumps over the lazy dog"
# Split the sentence into words
words = sentence.split(" ")

# Create an uneditable textbox at the top
st.text(
    "Correct words will be shown here with green underline. Incorrect words will be shown with red strikethrough along with correct word."
)

# Create a form
with st.form(key="word_form"):
    # Create a text input in the form
    user_word = st.text_input(label="Enter a word")
    # Create a submit button in the form
    submit_button = st.form_submit_button(label="Submit")

if "word_index" not in st.session_state:
    st.session_state["word_index"] = 0
    st.session_state["all_words"] = []
    st.session_state["user_score"] = 0


def update_textbox(word, correct_word, is_correct):
    if is_correct:
        return f'<u style="color: green">{word}</u>'
    else:
        return f'<del style="color: red">{word}</del> {correct_word}'


# Check if the form is submitted
if submit_button:
    word_index = st.session_state["word_index"]
    is_word_correct = user_word == words[word_index]
    st.session_state.all_words.append(
        update_textbox(user_word, words[word_index], is_word_correct)
    )
    st.session_state["word_index"] += 1
    st.session_state["user_score"] += 1 if is_word_correct else 0


st.write(st.session_state["word_index"])

if submit_button:
    st.write(
        "User score",
        st.session_state.user_score,
        "out of ",
        st.session_state.word_index,
    )

st.markdown(" ".join(st.session_state.all_words), unsafe_allow_html=True)
