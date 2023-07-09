import streamlit as st

from funcs import (
    check_token,
    get_ai_next_token,
    get_new_sentence_tokens,
    update_textbox,
)

st.set_page_config(
    layout="wide",
    page_title="LLM-ARP: You vs Transformer",
    page_icon="🤖",
    menu_items={"About": "# LLM-ARP: You vs Transformer"},
)


def set_game():
    st.session_state["word_index"] = 0
    st.session_state["all_words"] = []
    st.session_state["ai_words"] = []
    st.session_state["user_score"] = 0
    st.session_state["ai_score"] = 0
    st.session_state["user_word"] = ""
    sentence, sentence_tokens = get_new_sentence_tokens()
    st.session_state["sentence"] = sentence
    st.session_state["sentence_tokens"] = sentence_tokens


if "word_index" not in st.session_state:
    set_game()

words = st.session_state["sentence_tokens"]

st.title("🤖 LLM-ARP")
st.text("Playing as a Language Model")
with st.sidebar:
    st.write("Powered By OpenAI")
    reset_button, reveal_button = [st.button("Reset game"), st.button("Reveal text")]
    model_name = st.selectbox(
        label="Model",
        options=[
            "text-davinci-003",
            "ada",
        ],
    )
    st.image("assets/mechanical_hands.png")

if reset_button:
    set_game()

if reveal_button:
    st.session_state.word_index = len(words)

if st.session_state.word_index < len(words):
    with st.expander("Instructions"):
        st.write(
            "Pretend to be a Language Model. Please guess the next token in the sequence of random text from the web or Wikipedia. The sequence will start empty (guess the first word) and then you will be building up the sequence one word at a time.",
            "Correct words will be shown with green underline. Incorrect words will be shown with red strikethrough along with correct word.",
            "Ordinarily tokens can include spaces at the start but we'll allow tokens to be entered without spaces for this game.",
        )

    word_index = st.session_state["word_index"]
    top_container = st.container()

    input_word = st.text_input(value="", label="Enter a word")
    st.session_state.user_word = input_word.strip()

    user_word = st.session_state.user_word
    if user_word:
        top_container.subheader("Text so far:")
        top_container.progress(word_index / (len(words) - 1))
        top_container.write(" ".join(words[: word_index + 1]))

        is_word_correct = check_token(user_word, words[word_index])

        model_name = model_name or "ada"
        ai_word = get_ai_next_token(words[:word_index], model_name=model_name)
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
    st.write(st.session_state.sentence)

user_col, ai_col = st.columns(2)

with user_col:
    user_component = st.chat_message("user")
    user_score_message = (
        f"User score {st.session_state.user_score} out of {st.session_state.word_index}"
    )
    user_component.write(user_score_message)
    user_component.markdown(
        " ".join(st.session_state.all_words), unsafe_allow_html=True
    )

with ai_col:
    ai_component = st.chat_message("assistant")
    ai_score_message = (
        f"AI score {st.session_state.ai_score} out of {st.session_state.word_index}"
    )
    ai_component.write(ai_score_message)
    ai_component.markdown(" ".join(st.session_state.ai_words), unsafe_allow_html=True)
