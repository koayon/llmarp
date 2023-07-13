import streamlit as st

from funcs import (
    check_token,
    get_ai_next_token,
    get_new_sentence_tokens,
    update_textbox,
)
from gpt2_attention import predict_with_attention, show_attention
from text_copy import ATTENTION_CLICK, ATTENTION_EXPLAINER, INSTRUCTION_COPY

st.set_page_config(
    layout="wide",
    page_title="LLM-ARP: You vs Transformer",
    page_icon="🤖",
    menu_items={"About": "# LLM-ARP: You vs Transformer"},
)


def set_game(model_name="text-davinci-003"):
    # global input_word
    # input_word = ""

    st.session_state["word_index"] = 0
    st.session_state["all_words"] = []
    st.session_state["ai_words"] = []
    st.session_state["user_score"] = 0
    st.session_state["ai_score"] = 0
    st.session_state["user_word"] = ""
    sentence, sentence_tokens, url = get_new_sentence_tokens(model_name=model_name)
    st.session_state["sentence"] = sentence
    st.session_state["sentence_tokens"] = sentence_tokens
    st.session_state["attention_mode"] = False
    st.session_state["wiki_url"] = url
    st.session_state["gpt2_prediction_list"] = None
    st.session_state["layer"] = 0


if "word_index" not in st.session_state:
    set_game()

words = st.session_state["sentence_tokens"]

st.title("🤖 LLM-ARP")
st.text("LLM Action Role-Playing")
with st.sidebar:
    st.write("🧑 vs 🤖")
    reset_button, reveal_button = [st.button("Reset game"), st.button("Reveal text")]
    with st.form("model_form"):
        model_name = st.selectbox(
            label="Model",
            options=["text-davinci-003", "ada", "gpt2 with attention"],
        )
        submit_model = st.form_submit_button("Use this model")
        st.write(
            "Try using GPT-2 for a peek into attention! It might take a few seconds to load the model."
        )
        if submit_model and model_name:
            set_game(model_name=model_name)
    st.image("assets/mechanical_hands.png")

    st.write("Powered by Wikipedia, OpenAI and CircuitVis")

if reset_button:
    set_game()

if reveal_button:
    st.session_state.word_index = len(words)

if model_name == "gpt2 with attention":
    st.session_state["gpt2_prediction_list"] = st.session_state[
        "gpt2_prediction_list"
    ] or predict_with_attention(st.session_state.sentence)

if st.session_state.word_index < len(words):
    with st.expander("How To Play"):
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
            ai_word = (
                st.session_state.gpt2_prediction_list[word_index].best_guess
                if word_index > 0
                else "The"
            )
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
        if st.session_state.attention_mode:
            with attention_container:
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

                attention_component_html = show_attention(
                    tokens=prediction.str_tokens,
                    attention_pattern=prediction.attention_pattern,
                    active_layer=st.session_state.layer,
                )
                st.components.v1.html(attention_component_html, height=400)  # type: ignore

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
    st.info("Game over!")
    st.subheader(f"The full text was from {st.session_state.wiki_url} and reads:")
    st.write(st.session_state.sentence)

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
