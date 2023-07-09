# Functions
import openai
import streamlit as st
import tiktoken

from wiki import get_random_wiki_text

openai.api_key = st.secrets["OPENAI_API_KEY"]


def update_textbox(word, correct_word, is_correct):
    if is_correct:
        return f'<u style="color: green">{word}</u>'
    else:
        return f'<del style="color: red">{word}</del> {correct_word}'


def get_ai_next_token(start_of_sentence, model_name="ada"):
    if start_of_sentence:
        openai_response = openai.Completion.create(
            model=model_name,
            prompt="".join(start_of_sentence),
            temperature=0,
            max_tokens=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return openai_response.choices[0].text  # type: ignore
    else:
        return "The"


def tokenize_sentence(sentence):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(sentence)
    try:
        tokens_strs = [
            encoding.decode_single_token_bytes(token).decode() for token in tokens
        ]
    except UnicodeDecodeError:
        raise Exception("Unable to decode tokens from sentence.")
    tokens_strs = [token for token in tokens_strs if token.strip() != ""]
    # print(tokens_strs)
    return tokens_strs


def get_new_sentence_tokens():
    # sentence = "The quick brown hippopotamus jumps over the lazy dog"
    sentence = get_random_wiki_text()
    sentence_token_strs = tokenize_sentence(sentence)
    return sentence, sentence_token_strs


def check_token(candidate_token, target_token):
    candidate_token = candidate_token.lower().strip()
    target_token = target_token.lower().strip()
    return candidate_token == target_token
