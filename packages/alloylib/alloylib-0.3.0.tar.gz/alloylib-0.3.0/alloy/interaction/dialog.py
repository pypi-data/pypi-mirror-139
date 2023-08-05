# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
Operations useful for dialogs.
"""

import re
import typing


def split_sentences(text:str) -> typing.List[str]:
    """Split multiple sentences in one string into a list. Each item being a sentence.

    Args:
        text (str): Incoming string with multiple sentences.

    Returns:
        typing.List[str]: list of sentences.
    """
    SEP_REGEX = r"[^.!?]+[.!?]"


    sentences = []
    text_index = 0

    # try finding all and ensure its a valid match
    match: re.Match
    for match in re.finditer(SEP_REGEX, text):
        if match:
            sub_text = match.string[match.start():match.end()]
            if sub_text != "":
                sentences.append(sub_text.strip())
            text_index = match.end() + 1

    if text_index < len(text):
        remaining_text = text[text_index:]
        sentences.append(f"{remaining_text.strip()}.")

    return sentences