import streamlit as st

# Set the sentence in memory but not displayed
sentence = "The quick brown fox jumps over the lazy dog"
# Split the sentence into words
words = sentence.split(" ")
# Initialize the current word index
word_index = 0


# Function to update the textbox
def update_textbox(word, correct_word):
    # Show the correct word with green underline if the word is correct
    if word == correct_word:
        st.markdown(f'<u style="color: green">{word}</u>', unsafe_allow_html=True)
    # Else, show the correct word and the wrong word with red strikethrough
    else:
        st.markdown(
            f'<del style="color: red">{word}</del> {correct_word}',
            unsafe_allow_html=True,
        )


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

# Check if the form is submitted
if submit_button:
    # If the user word is the same as the next word in the sentence
    if user_word == words[word_index]:
        update_textbox(user_word, words[word_index])
        word_index += 1
    # If the user word is not the same
    else:
        update_textbox(user_word, words[word_index])
        word_index += 1
