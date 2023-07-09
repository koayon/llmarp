import openai
import streamlit as st
import tiktoken

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Functions


def update_textbox(word, correct_word, is_correct):
    if is_correct:
        return f'<u style="color: green">{word}</u>'
    else:
        return f'<del style="color: red">{word}</del> {correct_word}'


def get_ai_next_token(start_of_sentence):
    if start_of_sentence:
        openai_response = openai.Completion.create(
            model="text-davinci-003",
            prompt="".join(start_of_sentence),
            temperature=0,
            max_tokens=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print(openai_response)
        return openai_response.choices[0].text.strip()  # type: ignore
    else:
        return "The"


def tokenize_sentence(sentence):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(sentence)
    tokens_strs = [
        encoding.decode_single_token_bytes(token).decode() for token in tokens
    ]
    return tokens_strs


def set_game():
    st.session_state["word_index"] = 0
    st.session_state["all_words"] = []
    st.session_state["ai_words"] = []
    st.session_state["user_score"] = 0
    st.session_state["ai_score"] = 0
    st.session_state["user_word"] = ""
    st.session_state["sentence_tokens"] = get_new_sentence_tokens()


def get_new_sentence_tokens():
    sentence = "The quick brown hippopotamus jumps over the lazy dog"
    sentence_token_strs = tokenize_sentence(sentence)
    return sentence_token_strs


def check_token(candidate_token, target_token):
    candidate_token = candidate_token.lower()
    target_token = target_token.lower().strip()
    return candidate_token == target_token


if "word_index" not in st.session_state:
    set_game()

words = st.session_state["sentence_tokens"]

# UI

reset_button = st.button("Reset game")
if reset_button:
    set_game()

if st.session_state["word_index"] <= len(words):
    st.info(
        "Correct words will be shown with green underline. Incorrect words will be shown with red strikethrough along with correct word."
    )

    input_word = st.text_input(value="", label="Enter a word")
    st.session_state.user_word = input_word.strip()

    user_word = st.session_state.user_word
    if user_word:
        word_index = st.session_state["word_index"]
        is_word_correct = check_token(user_word, words[word_index])

        ai_word = get_ai_next_token(words[:word_index])
        is_ai_correct = check_token(ai_word, words[word_index])

        st.session_state.all_words.append(
            update_textbox(user_word, words[word_index], is_word_correct)
        )
        st.session_state.ai_words.append(
            update_textbox(ai_word, words[word_index], is_ai_correct)
        )
        st.session_state["word_index"] += 1
        st.session_state["user_score"] += 1 if is_word_correct else 0
        st.session_state["ai_score"] += 1 if is_ai_correct else 0

else:
    st.write("Game over!")

user_col, ai_col = st.columns(2)

with user_col:
    st.write(
        "User score",
        st.session_state.user_score,
        "out of ",
        st.session_state.word_index,
    )
    st.markdown(" ".join(st.session_state.all_words), unsafe_allow_html=True)

with ai_col:
    st.write(
        "AI score",
        st.session_state.ai_score,
        "out of ",
        st.session_state.word_index,
    )
    st.markdown(" ".join(st.session_state.ai_words), unsafe_allow_html=True)
