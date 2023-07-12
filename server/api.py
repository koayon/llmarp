from functools import partial
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import einops
import numpy as np
import pandas as pd
import torch
import transformer_lens
import transformer_lens.utils as utils
from fancy_einsum import einsum
from fastapi import FastAPI
from transformer_lens import ActivationCache, HookedTransformer

# Setup

torch.set_grad_enabled(False)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Looking at GPT-2 Small first
model = HookedTransformer.from_pretrained("gpt2", device=device)
model_cfg = model.cfg


def get_next_token(sequence: str, model: HookedTransformer = model) -> str:
    tokens = model.to_tokens(sequence)
    next_token = model(tokens).argmax(-1)
    # TODO: Also return the probability of the next token and maybe top 3 guesses
    return model.to_string(next_token)


def attention_pattern(sequence: str, model: HookedTransformer = model) -> list:
    logits, cache = model.run_with_cache(sequence, remove_batch_dim=True)
    attention_patterns = [cache["pattern", layer, "attn"] for layer in range(12)]
    attention_patterns = torch.stack(attention_patterns, dim=0)  # layer, head, seq, seq
    reduced_attention = einops.reduce(
        attention_patterns, "layer head i j -> i j", "mean"
    )
    final_token_attention = reduced_attention[-1]
    final_token_attention = final_token_attention[1:]
    # rescale to sum to 1
    final_token_attention = final_token_attention / final_token_attention.sum(
        -1, keepdims=True
    )
    return final_token_attention.numpy().tolist()


def predict_with_attention(sequence="1,2,3,4,", model=model):
    next_token = get_next_token(sequence, model)

    attention = attention_pattern(sequence, model)
    print("next token: ", next_token)
    print("attention: ", attention)
    return next_token, attention


if __name__ == "__main__":
    print(predict_with_attention("1,2,3,4,"))

# next_token_logits, cache = model.run_with_cache(to_4_seq)
# possible_next_tokens = next_token_logits.argsort(-1, descending=True)[0][-1][:10]
# print(possible_next_tokens.shape)
# model.to_str_tokens(possible_next_tokens.unsqueeze(0))

# to_4_seq = "1,2,3,4,"
# to_4_tokens = model.to_tokens(to_4_seq)
# logits, cache = model.run_with_cache(to_4_tokens, remove_batch_dim=True)

# attention_patterns = [cache["pattern", layer, "attn"] for layer in range(12)]
# attention_patterns = torch.stack(attention_patterns, dim=0)  # layer, head, seq, seq
# reduced_attention = einops.reduce(attention_patterns, "layer head i j -> i j", "mean")
# final_token_attention = reduced_attention[-1]
# final_token_attention = final_token_attention[1:]
# # rescale to sum to 1
# final_token_attention = final_token_attention / final_token_attention.sum(
#     -1, keepdims=True
# )


# # Also give how confident model was in it's prediction.
# next_token_probs = logits.softmax(-1)[0][-1].sort(descending=True)[0][:10]
