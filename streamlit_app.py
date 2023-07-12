import streamlit as st
from circuitsvis.attention import attention_patterns as cv_show_attention

from funcs import (
    check_token,
    get_ai_next_token,
    get_new_sentence_tokens,
    update_textbox,
)
from gpt2_attention import predict_with_attention
from text_copy import ATTENTION_CLICK, ATTENTION_EXPLAINER, INSTRUCTION_COPY

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
    sentence, sentence_tokens = get_new_sentence_tokens(model_name="text-davinci-003")
    st.session_state["sentence"] = sentence
    st.session_state["sentence_tokens"] = sentence_tokens
    st.session_state["attention_mode"] = False


if "word_index" not in st.session_state:
    set_game()

words = st.session_state["sentence_tokens"]

st.title("🤖 LLM-ARP")
st.text("Playing as a Language Model")
with st.sidebar:
    st.write("🧑 vs 🤖")
    # st.write("Powered By OpenAI")
    reset_button, reveal_button = [st.button("Reset game"), st.button("Reveal text")]
    model_name = st.selectbox(
        label="Model",
        options=["text-davinci-003", "ada", "gpt2 with attention"],
    )
    st.image("assets/mechanical_hands.png")

if reset_button:
    set_game()

if reveal_button:
    st.session_state.word_index = len(words)

if st.session_state.attention_mode:
    st.session_state["gpt2_prediction_list"] = predict_with_attention(
        st.session_state.sentence
    )

if st.session_state.word_index < len(words):
    with st.expander("Instructions"):
        st.write(INSTRUCTION_COPY)

    word_index = st.session_state["word_index"]
    top_container = st.container()

    input_word = st.text_input(value="", label="Enter a word")

    user_col, ai_col = st.columns(2)

    if model_name == "gpt2 with attention":
        st.session_state.attention_mode = st.checkbox("Show attention patterns 🧠")

        attention_container = st.container()

    st.session_state.user_word = input_word.strip()

    user_word = st.session_state.user_word

    if user_word:
        top_container.subheader("Text so far:")
        top_container.progress(word_index / (len(words) - 1))
        top_container.write(" ".join(words[: word_index + 1]))

        is_word_correct = check_token(user_word, words[word_index])

        model_name = model_name or "ada"
        if model_name == "gpt2 with attention":
            ai_word = st.session_state.gpt2_prediction_list[word_index].best_guess
        else:
            ai_word = get_ai_next_token(words[:word_index], model_name=model_name)
        is_ai_correct = check_token(ai_word, words[word_index])
        # TODO: Check AI score for GPT-2 case

        st.session_state.all_words.append(
            update_textbox(user_word, words[word_index], is_word_correct)
        )
        st.session_state.ai_words.append(
            update_textbox(ai_word, words[word_index], is_ai_correct)
        )
        st.session_state["word_index"] += 1
        st.session_state["user_score"] += 1 if is_word_correct else 0
        st.session_state["ai_score"] += 1 if is_ai_correct else 0

        with attention_container:
            if st.session_state.attention_mode:
                # st.write(
                #     st.session_state.gpt2_prediction_list[50].str_tokens,
                # )
                # st.write(
                #     st.session_state.sentence_tokens,
                # )

                st.subheader("Attention patterns")
                with st.expander("What are attention patterns and how to I read them?"):
                    st.write(ATTENTION_EXPLAINER)

                prediction = st.session_state.gpt2_prediction_list[word_index]

                layer = st.slider("Layer", 0, 11, 0)
                st.write("Attention pattern for layer", layer)
                attention_html = cv_show_attention(
                    tokens=prediction.str_tokens,
                    attention=prediction.attention_pattern[layer],
                ).show_code()
                st.components.v1.html(attention_html, height=400)  # type: ignore

                st.subheader(ATTENTION_CLICK)

    with user_col:
        user_component = st.chat_message("user")
        user_score_message = f"User score {st.session_state.user_score} out of {st.session_state.word_index}"
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
        ai_component.markdown(
            " ".join(st.session_state.ai_words), unsafe_allow_html=True
        )

else:
    st.write("Game over!")
    st.write(st.session_state.sentence)
