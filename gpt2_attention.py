"""Idea:
You give me a sequence of tokens, for each subsequence I give you back:
- The best prediction for next token
- How confident I am
- My top 5 guesses
- The attention pattern I used to get this guess"""


from dataclasses import dataclass
from typing import Dict, List, Tuple

import torch
from transformer_lens import HookedTransformer

# Setup

torch.set_grad_enabled(False)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Looking at GPT-2 Small first
model = HookedTransformer.from_pretrained("gpt2", device=device)
model_cfg = model.cfg


def get_all_predictions(
    sequence: str, model: HookedTransformer = model, topk: int = 5
) -> Tuple[List[str], List[float], List[List[str]]]:
    "Return next guess for each substring, confidence in the guess and top 5 guesses"
    with torch.inference_mode():
        logits = model(sequence)  # batch (1), sequence length, vocab size

    logits_most_to_least_likely, tokens_most_to_least_likely = logits.sort(
        -1, descending=True
    )  # batch (1), sequence length, vocab size
    # print(logits_most_to_least_likely.shape)

    probs_most_to_least_likely = torch.softmax(logits_most_to_least_likely, dim=-1)[0]
    confidence_in_top_guesses = probs_most_to_least_likely[:, 0].numpy().tolist()
    confidence_in_top_guesses = [
        round(confidence, 3) for confidence in confidence_in_top_guesses
    ]

    top_predictions = tokens_most_to_least_likely[0, :, :topk]  # sequence length, topk

    topk_predictions = []
    for i, token in enumerate(top_predictions):
        topk_predictions.append(model.to_str_tokens(top_predictions[i]))

    best_guesses = [guess[0] for guess in topk_predictions]

    # print(top_predictions.shape)
    # print(top_predictions)

    # topk_predictions = model.to_str_tokens(final_top_predictions)
    return best_guesses, confidence_in_top_guesses, topk_predictions


def attention_pattern(
    sequence: str, model: HookedTransformer = model
) -> Tuple[List, List]:
    with torch.inference_mode():
        _logits, cache = model.run_with_cache(sequence, remove_batch_dim=True)
    attention_patterns = [cache["pattern", layer, "attn"] for layer in range(12)]

    str_tokens = model.to_str_tokens(sequence)

    return attention_patterns, str_tokens


# attention_patterns, str_tokens = attention_pattern(sequence="1,2,3,4,")
# # Showing the attention patterm
# layer = 7
# print(f"Layer {layer} attention patterns")
# cv_show_attention(tokens=str_tokens, attention=attention_patterns[layer])


@dataclass
class Prediction:
    best_guess: str
    confidence_in_top_guesses: float
    topk_predictions: List[str]
    attention_pattern: List[torch.Tensor]
    str_tokens: List[str]


@dataclass
class PredictionList:
    best_guesses: List[str]
    confidence_in_top_guesses: List[float]
    topk_predictions: List[List[str]]
    attention_patterns: List[torch.Tensor]
    str_tokens: List[str]

    def __getitem__(self, index):
        # Currently a (layer) list of head, i, j attention patterns
        indexed_attention_patterns = []
        for layer in self.attention_patterns:
            indexed_attention_patterns.append(layer[:, : index + 1, : index + 1])

        return Prediction(
            best_guess=self.best_guesses[index],
            confidence_in_top_guesses=self.confidence_in_top_guesses[index],
            topk_predictions=self.topk_predictions[index],
            attention_pattern=indexed_attention_patterns,
            str_tokens=self.str_tokens[: index + 1],
        )


def predict_with_attention(
    sequence: str = "1,2,3,4,", model: HookedTransformer = model
) -> PredictionList:
    best_guesses, confidence_in_top_guesses, topk_predictions = get_all_predictions(
        sequence, model
    )

    attention_patterns, str_tokens = attention_pattern(sequence, model)

    prediction_list = PredictionList(
        best_guesses=best_guesses,
        confidence_in_top_guesses=confidence_in_top_guesses,
        topk_predictions=topk_predictions,
        attention_patterns=attention_patterns,
        str_tokens=str_tokens,
    )
    return prediction_list


if __name__ == "__main__":
    predictions = predict_with_attention()
    print("----------------------------------")
    print("Predicting first token...")
    print(predictions[0])
    print("----------------------------------")
    print("Predicting 5th token...")
    print(predictions[4])
