INSTRUCTION_COPY = (
    "Pretend to be a Language Model. Please guess the next token in the sequence of random text from the web or Wikipedia. The sequence will start empty (guess the first word) and then you will be building up the sequence one word at a time.",
    "Correct words will be shown with green underline. Incorrect words will be shown with red strikethrough along with correct word.",
    "Ordinarily tokens can include spaces at the start but we'll allow tokens to be entered without spaces for this game.",
)

ATTENTION_EXPLAINER = """Here you can look inside the AI's brain andexamine the attention patterns of the GPT-2 model for the paragraph you're completing.
The attention patterns show which words the model is focusing on to help it to make it's eventual decision.

GPT-2 as a model is a transformer model with 12 layers and 12 attention heads on each layer.

You can use the slider to select which layer you want to look at and hover over the different heads to focus on that head.
The darker the colour, the more attention the model is paying to that word."""

ATTENTION_CLICK = """Click on the final word above to see where the model was paying attention to when guessing that word."""
