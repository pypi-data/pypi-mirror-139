from wsln.lexer import Token, Phrase, Sentence, TokenTag, merge_same_tags, merge_by_phrase_rule, PhraseRule, tokenize_text, segment_sentences


def test_phrase():
    test_cases = [
        (
            Phrase([
                Token("template", TokenTag.NOUN),
                Token("pattern", TokenTag.NOUN),
            ], TokenTag.NOUN),
            "template pattern",
        ),
    ]

    for input, expected in test_cases:
        assert input.text == expected


def test_merge_same_tags():

    test_cases = [
        (
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("link", TokenTag.NOUN),
                Token("boy", TokenTag.NOUN),
            ],
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Phrase([
                    Token("link", TokenTag.NOUN),
                    Token("boy", TokenTag.NOUN),
                ], TokenTag.NOUN)
            ],
        ),
        (
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("link", TokenTag.NOUN),
                Token("boy", TokenTag.NOUN),
                Token("girl", TokenTag.NOUN),
                Token("man", TokenTag.NOUN),
            ],
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Phrase([
                    Token("link", TokenTag.NOUN),
                    Token("boy", TokenTag.NOUN),
                    Token("girl", TokenTag.NOUN),
                    Token("man", TokenTag.NOUN),
                ], TokenTag.NOUN)
            ],
        )
    ]

    for input_tokens, expected_tokens in test_cases:
        merged_tokens = merge_same_tags(input_tokens)

        assert merged_tokens == expected_tokens


def test_merge_by_phrase_rule(phrase_rules):
    test_cases = [
        (
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("good", TokenTag.ADJ),
                Token("boy", TokenTag.NOUN),
            ],
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Phrase([
                    Token("good", TokenTag.ADJ),
                    Token("boy", TokenTag.NOUN),
                ], TokenTag.NOUN)
            ],
        ),
        (
            [
                Token("love", TokenTag.VERB),
                Token("baby", TokenTag.NOUN),
            ],
            [
                Token("love", TokenTag.VERB),
                Token("baby", TokenTag.NOUN),
            ],
        ),
        (
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("good", TokenTag.ADJ),
                Token("boy", TokenTag.NOUN),
                Token("ha", TokenTag.INTERJECTION),
            ],
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Phrase([
                    Token("good", TokenTag.ADJ),
                    Token("boy", TokenTag.NOUN),
                ], TokenTag.NOUN),
                Token("ha", TokenTag.INTERJECTION),
            ],
        ),
        (
            [
                Token("very", TokenTag.ADV),
                Token("good", TokenTag.ADJ),
                Token("boy", TokenTag.NOUN),
            ],
            [
                Phrase([
                    Phrase([
                        Token("very", TokenTag.ADV),
                        Token("good", TokenTag.ADJ),
                    ], TokenTag.ADJ),
                    Token("boy", TokenTag.NOUN),
                ], TokenTag.NOUN)
            ]
        ),
        (
            [
                Token("five", TokenTag.NUMERAL),
                Token("key", TokenTag.ADJ),
                Token("states", TokenTag.NOUN),
            ],
            [
                Phrase([
                    Token("five", TokenTag.NUMERAL),
                    Phrase([
                        Token("key", TokenTag.ADJ),
                        Token("states", TokenTag.NOUN),
                    ], TokenTag.NOUN),
                ], TokenTag.NOUN)
            ]
        )
    ]

    for input_tokens, expected_tokens in test_cases:
        merged_tokens = merge_by_phrase_rule(input_tokens, phrase_rules)

        assert merged_tokens == expected_tokens


def test_segment_sentences():
    test_cases = [
        (
            "This is sentence 1. This is sentence 2, phrase 1. This is sentence 3; This is sentence 4! What is sentence (5) ?Haha",
            [
                "This is sentence 1 .",
                "This is sentence 2 , phrase 1 .",
                "This is sentence 3 ; This is sentence 4 !",
                "What is sentence ( 5 ) ?",
                "Haha",
            ]
        )
    ]

    for input_text, expected_sentences in test_cases:
        sentences = segment_sentences(input_text)
        assert sentences == expected_sentences

def test_nltk_tokenizer():
    test_cases = [
        (
            "Jack is a good boy(five).",
            Sentence([
                Token("Jack", TokenTag.NOUN), 
                Token("is", TokenTag.VERB), 
                Token("a", TokenTag.ARTICLE), 
                Token("good", TokenTag.ADJ), 
                Token("boy", TokenTag.NOUN), 
                Token("(", TokenTag.PUNCTUATION), 
                Token("five", TokenTag.NUMERAL), 
                Token(")", TokenTag.PUNCTUATION), 
                Token(".", TokenTag.PUNCTUATION)
            ]),
        )
    ]

    for input_sentence, expected_tokens in test_cases:
        assert tokenize_text(input_sentence) == expected_tokens


def test_new_sentence():
    test_cases = [
        (
            "Jack is a good boy (five).",
            Sentence([
                Token("Jack", TokenTag.NOUN), 
                Token("is", TokenTag.VERB), 
                Token("a", TokenTag.ARTICLE), 
                Phrase([
                    Token("good", TokenTag.ADJ), 
                    Token("boy", TokenTag.NOUN), 
                ], TokenTag.NOUN),
                Token("(", TokenTag.PUNCTUATION),
                Token("five", TokenTag.NUMERAL), 
                Token(")", TokenTag.PUNCTUATION), 
                Token(".", TokenTag.PUNCTUATION)
            ]),
        ),
        (
            [
                Token("Jack", TokenTag.NOUN), 
                Token("is", TokenTag.VERB), 
                Token("a", TokenTag.ARTICLE), 
                Phrase([
                    Token("good", TokenTag.ADJ), 
                    Token("boy", TokenTag.NOUN), 
                ], TokenTag.NOUN),
                Token("(", TokenTag.PUNCTUATION), 
                Token("five", TokenTag.NUMERAL), 
                Token(")", TokenTag.PUNCTUATION), 
                Token(".", TokenTag.PUNCTUATION)
            ],
            Sentence("Jack is a good boy (five)."),
        ),
    ]

    for input, expected_sentence in test_cases:
        assert Sentence(input) == expected_sentence


def test_sentence_noun_snippets():
    test_cases = [
        (
            Sentence([
                Token("The", TokenTag.ARTICLE),
                Token("Pattern", TokenTag.NOUN),
                Token("consists", TokenTag.VERB),
                Token("of", TokenTag.PREPOSITION),
                Token("two", TokenTag.NUMERAL),
                Token("node", TokenTag.NOUN),
                Token("indicators", TokenTag.NOUN),
                Token("and", TokenTag.CONJUNCTION),
                Token("a", TokenTag.ARTICLE),
                Token("link", TokenTag.NOUN),
                Token("indicator", TokenTag.NOUN),
                Token("to", TokenTag.PREPOSITION),
                Token("extract", TokenTag.VERB),
                Token("links", TokenTag.NOUN),
                Token("ha", TokenTag.INTERJECTION)
            ]),
            [
                [
                    Token("The", TokenTag.ARTICLE),
                    Token("Pattern", TokenTag.NOUN),
                ],
                [
                    Token("Pattern", TokenTag.NOUN),
                    Token("consists", TokenTag.VERB),
                    Token("of", TokenTag.PREPOSITION),
                    Token("two", TokenTag.NUMERAL),
                    Token("node", TokenTag.NOUN)
                ],
                [
                    Token("node", TokenTag.NOUN),
                    Token("indicators", TokenTag.NOUN),
                ],
                [
                    Token("indicators", TokenTag.NOUN),
                    Token("and", TokenTag.CONJUNCTION),
                    Token("a", TokenTag.ARTICLE),
                    Token("link", TokenTag.NOUN),
                ],
                [
                    Token("link", TokenTag.NOUN),
                    Token("indicator", TokenTag.NOUN),
                ],
                [
                    Token("indicator", TokenTag.NOUN),
                    Token("to", TokenTag.PREPOSITION),
                    Token("extract", TokenTag.VERB),
                    Token("links", TokenTag.NOUN),
                ],
                [
                    Token("links", TokenTag.NOUN),
                    Token("ha", TokenTag.INTERJECTION),
                ]
            ]
        ),
        (
            Sentence([
                Token("Pattern", TokenTag.NOUN),
                Token("consists", TokenTag.VERB),
                Token("of", TokenTag.PREPOSITION),
                Token("two", TokenTag.NUMERAL),
                Token("node", TokenTag.NOUN),
            ]),
            [
                [
                    Token("Pattern", TokenTag.NOUN),
                    Token("consists", TokenTag.VERB),
                    Token("of", TokenTag.PREPOSITION),
                    Token("two", TokenTag.NUMERAL),
                    Token("node", TokenTag.NOUN)
                ],
            ]
        ),
    ]

    for input_sentence, expected_snippets in test_cases:
        assert input_sentence.noun_snippets == expected_snippets
