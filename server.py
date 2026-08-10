#!/usr/bin/env python3

import sys
from json import load
from typing import Annotated
from urllib.parse import quote
from urllib.request import urlopen

from mcp.server import MCPServer
from pydantic import Field


# Create the MCP server.
mcp = MCPServer("demo-server")

@mcp.tool(title="English news: Get word frequency")
def english_word_frequency(
    input_word: Annotated[
        str,
        Field(
            description=(
                "Required. A single English word to look up in the supplied 2025 English news corpus. "
                "Example: climate"
            )
        ),
    ],
    case_sensitive: Annotated[
        bool,
        Field(
            description=(
                "Optional. Set to true only when the user requests a case-sensitive lookup. "
                "Default: false."
            )
        ),
    ] = False,
    part_of: Annotated[
        bool,
        Field(
            description=(
                "Optional. Set to true to total the counts of all dataset entries that contain the "
                "supplied text, instead of requiring an exact match. Default: false."
            )
        ),
    ] = False,
) -> dict:
    """
    Returns the total count for matching entries in the supplied English news corpus.

    By default, this looks up one whole word without considering case. When
    `part_of` is true, it totals the counts of every dataset entry that contains
    the supplied text.

    If no entries match, the total count is 0. This does not prove that the word
    never occurs outside the supplied dataset.
    """
    print(
        "Tool english_word_frequency called with parameters: "
        f"input_word={input_word}, case_sensitive={case_sensitive}, part_of={part_of}",
        file=sys.stderr,
    )

    
    word = input_word.strip()

    if not case_sensitive:
        word = word.lower()

    total_count = 0 

    with open("data/eng_news_2025_100K-words.txt", encoding="utf-8") as frequency_file:

        for line in frequency_file:
            _, corpus_word, count = line.rstrip("\n").split("\t")
            comparison_word = corpus_word
            count = int(count)

            if not case_sensitive:
                comparison_word = corpus_word.lower()

            if part_of and word in comparison_word:
                total_count += count
            elif word == comparison_word:
               total_count += count
            
    return {"Total occurence:" : total_count}


@mcp.tool(title="English news: Get example sentences")
def english_example_sentences(
    word: Annotated[
        str,
        Field(
            description=(
                "Required. A single English word for which to retrieve example sentences from the "
                "external Leipzig Corpora Collection API. Example: climate"
            )
        ),
    ],
    limit: Annotated[
        int,
        Field(
            description=(
                "Optional. Maximum number of example sentences to return. Keep this small to avoid "
                "an oversized response. Default: 3."
            ),
            ge=1,  # Greater than or equal to 1.
            le=5,  # Less than or equal to 5.
        ),
    ] = 3,
) -> dict:
    """
    Returns example sentences from the external Leipzig Corpora Collection API.

    The examples come from the English news corpus.
    The response includes the total number of available sentences and up to the requested number of examples.
    """
    print(
        "Tool english_example_sentences called with parameters: "
        f"word={word}, limit={limit}",
        file=sys.stderr,
    )

    url = (
        "https://api.wortschatz-leipzig.de/ws/sentences/eng_news_2013_3M/sentences/"
        f"{quote(word.strip())}?limit={limit}"
    )

    with urlopen(url, timeout=10) as response:
        return load(response)


if __name__ == "__main__":
    try:
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=8000,
            stateless_http=True,
        )
    except KeyboardInterrupt:
        pass
