from wsln.lexer import Token, TokenTag, Phrase, Sentence
from wsln.parser import Symbol, Pattern, MatchedPattern, LinkType, PatternSetHandler, SemanticLink, SemanticNode, W_SLN, NULL_NODE


def test_new_pattern():
    cases = [
        (
            (
                "N1 V N2",
                "N1",
                "V",
                "action",
                "N2",
            ),
            [
                Symbol("N1"),
                Symbol("V"),
                Symbol("N2"),
            ],
            LinkType.ACTION,
        ),
        (
            (
                "N1 BE V N2",
                "N1",
                "V",
                "attribute",
                "N2",
            ),
            [
                Symbol("N1"),
                Symbol("BE"),
                Symbol("V"),
                Symbol("N2")
            ],
            LinkType.ATTRIBUTE,
        ),
        (
            (
                "N1 I23(don't|do not|never) V N22",
                "N1",
                "I23",
                "negative",
                "N22",
            ),
            [
                Symbol("N1"),
                Symbol("I23", ["don't", "do not", "never"]),
                Symbol("V"),
                Symbol("N22"),
            ],
            LinkType.NEGATIVE,
        ),
        (
            (
                "N1 V",
                "N1",
                "V",
                "action",
                None,
            ),
            [
                Symbol("N1"),
                Symbol("V"),
            ],
            LinkType.ACTION,
        ),
        (
            (
                "S1 I(if) S2",
                "S1",
                "I",
                LinkType.CAUSE_EFFECT,
                "S2",
            ),
            [
                Symbol("S1"),
                Symbol("I", ["if"]),
                Symbol("S2"),
            ],
            LinkType.CAUSE_EFFECT,
        ),
    ]

    for input, expected_symbols, expected_link_type in cases:
        pattern = Pattern(*input)
        assert pattern.symbols == expected_symbols
        assert pattern.link_type == expected_link_type


def test_symbol_match_tokens():
    test_cases = [
        (
            Symbol("I", ["does", "does not", "does not like", "don't", "which", "never"]),
            [
                Token("I", TokenTag.NOUN),
                Phrase([Token("does", TokenTag.VERB), Token("not", TokenTag.ADV)], TokenTag.VERB),
                Token("like", TokenTag.VERB),
            ],
            0,
        ),
        (
            Symbol("I", ["does", "does not", "does not like", "don't", "which", "never"]),
            [
                Phrase([Token("does", TokenTag.VERB), Token("not", TokenTag.VERB)], TokenTag.VERB),
                Token("love", TokenTag.VERB),
            ],
            1,
        ),
        (
            Symbol("I", ["does", "does not", "does not like", "don't", "which", "never"]),
            [
                Phrase([Token("does", TokenTag.VERB), Token("not", TokenTag.VERB)], TokenTag.VERB),
                Token("like", TokenTag.VERB),
            ],
            2,
        ),
    ]

    for symbol, tokens, offset in test_cases:
        assert offset == symbol.match_tokens(tokens)


def test_pattern_private_match_tokens():
    test_cases = [
        (
            Pattern("N1 V N2", "N1", "V", "action", "N2"),
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("nice", TokenTag.ADJ),
            ],
            []
        ),
        (

        )
    ]


def test_pattern_match_tokens():
    test_cases = [
        (
            Pattern(
                "N1 BE V",
                "N1",
                "BE",
                "attribute",
                "V",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("nice", TokenTag.ADJ),
            ],
            [],
        ),
        (
            Pattern(
                "N1 BE ADJ",
                "N1",
                "BE",
                "attribute",
                "ADJ",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("good", TokenTag.ADJ),
            ],
            [[
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("good", TokenTag.ADJ),
            ]],
        ),
        (
            Pattern(
                "N1 BE ADJ",
                "N1",
                "BE",
                "attribute",
                "ADJ",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Phrase([
                    Token("good", TokenTag.ADJ),
                    Token("good", TokenTag.ADJ),
                ], TokenTag.ADJ),
            ],
            [[
                Token("Jack", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Phrase([
                    Token("good", TokenTag.ADJ),
                    Token("good", TokenTag.ADJ),
                ], TokenTag.ADJ),
            ]],
        ),
        (
            Pattern(
                "N1 V N2",
                "N1",
                "V",
                "action",
                "N2",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("rob", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("car", TokenTag.NOUN),
            ],
            [[
                Token("Jack", TokenTag.NOUN),
                Token("rob", TokenTag.VERB),
                Token("car", TokenTag.NOUN),
            ]]
        ),
        (
            Pattern(
                "N1 V N2",
                "N1",
                "V",
                "action",
                "N2",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("rob", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("benz", TokenTag.NOUN),
                Token("car", TokenTag.NOUN),
            ],
            [
                [
                    Token("Jack", TokenTag.NOUN),
                    Token("rob", TokenTag.VERB),
                    Token("benz", TokenTag.NOUN),
                ],
                [
                    Token("Jack", TokenTag.NOUN),
                    Token("rob", TokenTag.VERB),
                    Token("car", TokenTag.NOUN),
                ]
            ]
        ),
        (
            Pattern(
                "N1 V",
                "N1",
                "V",
                "action",
                None,
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("rob", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("benz", TokenTag.NOUN),
                Token("car", TokenTag.NOUN),
            ],
            [[
                Token("Jack", TokenTag.NOUN),
                Token("rob", TokenTag.VERB),
            ]]
        ),
        (
            Pattern(
                "N1 V N2",
                "N1",
                "V",
                "action",
                "N2",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("rob", TokenTag.VERB),
                Token("and", TokenTag.CONJUNCTION),
                Token("burn", TokenTag.VERB),
                Token("car", TokenTag.NOUN),
            ],
            [
                [
                    Token("Jack", TokenTag.NOUN),
                    Token("rob", TokenTag.VERB),
                    Token("car", TokenTag.NOUN),
                ],
                [
                    Token("Jack", TokenTag.NOUN),
                    Token("burn", TokenTag.VERB),
                    Token("car", TokenTag.NOUN),
                ], 
            ]
        ),
        (
            Pattern(
                "N1 I2(don't|do not|does not|never) N2",
                "N1",
                "I2",
                "negative",
                "N2",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("does", TokenTag.VERB),
                Token("not", TokenTag.ADV),
                Token("football", TokenTag.NOUN),
            ],
            [
                [
                    Token("Jack", TokenTag.NOUN),
                    Phrase([
                        Token("does", TokenTag.VERB),
                        Token("not", TokenTag.ADV),
                    ]),
                    Token("football", TokenTag.NOUN),
                ],
            ],
        ),
        (
            Pattern(
                "N1 I2(don't|do not|does not|never) N2",
                "N1",
                "I2",
                "negative",
                "N2",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("never", TokenTag.ADV),
                Token("play", TokenTag.VERB),
                Token("football", TokenTag.NOUN),
            ],
            [[
                Token("Jack", TokenTag.NOUN),
                Token("never", TokenTag.ADV),
                Token("football", TokenTag.NOUN),
            ]],
        ),
        (
            Pattern(
                "N1 I2(don't|do not|does not|never) V N2",
                "N1",
                "I2",
                "negative",
                "N2",
            ),
            [
                Token("Jack", TokenTag.NOUN),
                Token("never", TokenTag.ADV),
                Token("play", TokenTag.VERB),
                Token("football", TokenTag.NOUN),
            ],
            [[
                Token("Jack", TokenTag.NOUN),
                Token("never", TokenTag.ADV),
                Token("play", TokenTag.VERB),
                Token("football", TokenTag.NOUN),
            ]],
        ),
        (
            Pattern(
                "N1 BE I(kind of) N2",
                "N1",
                "I",
                "abstract",
                "N2",
            ),
            [
                Token("Apple", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("a", TokenTag.ARTICLE),
                Token("kind", TokenTag.NOUN),
                Token("of", TokenTag.PREPOSITION),
                Token("fruit", TokenTag.NOUN),
            ],
            [[
                Token("Apple", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Phrase([
                    Token("kind", TokenTag.NOUN),
                    Token("of", TokenTag.PREPOSITION),
                ]),
                Token("fruit", TokenTag.NOUN),
            ]],
        ),
        (
            Pattern("S1 I(if|because) S2", "S1", "I", "cause-effect", "S2"),
            [
                Token("I", TokenTag.NOUN),
                Token("could", TokenTag.VERB),
                Token("do", TokenTag.VERB),
                Token("if", TokenTag.ADV),
                Token("you", TokenTag.NOUN),
                Token("like", TokenTag.VERB),
            ],
            [[
                [
                    Token("I", TokenTag.NOUN),
                    Token("could", TokenTag.VERB),
                    Token("do", TokenTag.VERB)
                ],
                Token("if", TokenTag.ADV),
                [
                    Token("you", TokenTag.NOUN),
                    Token("like", TokenTag.VERB),
                ],
            ]]
        ),
        (
            Pattern("S1 I(if|because|because of) S2", "S1", "I", "cause-effect", "S2"),
            [
                Token("I", TokenTag.NOUN),
                Token("could", TokenTag.VERB),
                Token("do", TokenTag.VERB),
                Token("if", TokenTag.ADV),
                Token("you", TokenTag.NOUN),
                Token("like", TokenTag.VERB),
                Token("because", TokenTag.ADV),
                Token("they", TokenTag.NOUN),
                Token("hate", TokenTag.VERB),
            ],
            [
                [
                    [
                        Token("I", TokenTag.NOUN),
                        Token("could", TokenTag.VERB),
                        Token("do", TokenTag.VERB),
                    ],
                    Token("if", TokenTag.ADV),
                    [
                        Token("you", TokenTag.NOUN),
                        Token("like", TokenTag.VERB),
                        Token("because", TokenTag.ADV),
                        Token("they", TokenTag.NOUN),
                        Token("hate", TokenTag.VERB),
                    ]
                ],
                [
                    [
                        Token("I", TokenTag.NOUN),
                        Token("could", TokenTag.VERB),
                        Token("do", TokenTag.VERB),
                        Token("if", TokenTag.ADV),
                        Token("you", TokenTag.NOUN),
                        Token("like", TokenTag.VERB),
                    ],
                    Token("because", TokenTag.ADV),
                    [
                        Token("they", TokenTag.NOUN),
                        Token("hate", TokenTag.VERB),
                    ]
                ],
            ]
        ),
        (
            Pattern("S1 I(if|because|because of) S2", "S1", "I", "cause-effect", "S2"),
            [
                Token("I", TokenTag.NOUN),
                Token("could", TokenTag.VERB),
                Token("do", TokenTag.VERB),
                Token("if", TokenTag.ADV),
                Token("you", TokenTag.NOUN),
                Token("like", TokenTag.VERB),
                Token("because", TokenTag.ADV),
                Token("of", TokenTag.PREPOSITION),
                Token("they", TokenTag.NOUN),
                Token("hate", TokenTag.VERB),
            ],
            [
                [
                    [
                        Token("I", TokenTag.NOUN),
                        Token("could", TokenTag.VERB),
                        Token("do", TokenTag.VERB),
                    ],
                    Token("if", TokenTag.ADV),
                    [
                        Token("you", TokenTag.NOUN),
                        Token("like", TokenTag.VERB),
                        Token("because", TokenTag.ADV),
                        Token("of", TokenTag.PREPOSITION),
                        Token("they", TokenTag.NOUN),
                        Token("hate", TokenTag.VERB),
                    ]
                ],
                [
                    [
                        Token("I", TokenTag.NOUN),
                        Token("could", TokenTag.VERB),
                        Token("do", TokenTag.VERB),
                        Token("if", TokenTag.ADV),
                        Token("you", TokenTag.NOUN),
                        Token("like", TokenTag.VERB),
                    ],
                    Phrase([
                        Token("because", TokenTag.ADV),
                        Token("of", TokenTag.PREPOSITION),
                    ]),
                    [
                        Token("they", TokenTag.NOUN),
                        Token("hate", TokenTag.VERB),
                    ]
                ],
            ]
        )
    ]

    for pattern, tokens, expected in test_cases:
        actual = pattern.match_tokens(tokens)
        assert actual == [
            MatchedPattern(pattern, expected_tokens)
            for expected_tokens in expected
        ]


def test_match_pattern_recursive_link():
    pattern_action1 = Pattern(
        "N1 V N2",
        from_id="N1",
        indicator="V",
        to_id="N2",
        link_type=LinkType.ACTION,
    )
    pattern_action2 = Pattern(
        "N1 V",
        from_id="N1",
        indicator="V",
        to_id=None,
        link_type=LinkType.ACTION,
    )
    pattern_if = Pattern(
        "S1 I(if) S2",
        "S1",
        "I",
        "cause-effect",
        "S2",
    )
    test_cases = [
        (
            [pattern_if, pattern_action1, pattern_action2],
            [
                Token("I", TokenTag.NOUN),
                Token("could", TokenTag.VERB),
                Token("do", TokenTag.VERB),
                Token("if", TokenTag.ADV),
                Token("you", TokenTag.NOUN),
                Token("like", TokenTag.VERB),
            ],
            [
                SemanticLink(
                    from_node=SemanticNode([SemanticLink(
                        SemanticNode(Token("I", TokenTag.NOUN)),
                        SemanticNode(
                            Token("could", TokenTag.VERB),
                        ),
                        LinkType.ACTION,
                        NULL_NODE,
                    ), SemanticLink(
                        SemanticNode(Token("I", TokenTag.NOUN)),
                        SemanticNode(Token("do", TokenTag.VERB),),
                        LinkType.ACTION,
                        NULL_NODE,
                    )]),
                    indicator_node=SemanticNode(Token("if", TokenTag.ADV)),
                    link_type=LinkType.CAUSE_EFFECT,
                    to_node=SemanticNode([SemanticLink(
                        SemanticNode(Token("you", TokenTag.NOUN)),
                        SemanticNode(Token("like", TokenTag.VERB)),
                        LinkType.ACTION,
                        NULL_NODE,
                    )]),
                )
            ],
        ),
    ]

    for patterns, tokens, expected_links in test_cases:
        ph = PatternSetHandler(patterns)
        matched_patterns = ph.match_tokens(tokens)
        assert [mp.to_link() for mp in matched_patterns] == expected_links


def test_pattern_set_handler_match_tokens():
    pattern_action1 = Pattern(
        "N1 V N2",
        from_id="N1",
        indicator="V",
        to_id="N2",
        link_type=LinkType.ACTION,
    )
    pattern_action2 = Pattern(
        "N1 V",
        from_id="N1",
        indicator="V",
        to_id="N1",
        link_type=LinkType.ACTION,
    )
    pattern_attr = Pattern(
        "N V ADJ",
        from_id="N",
        indicator="V",
        to_id="ADJ",
        link_type=LinkType.ATTRIBUTE,
    )
    pattern_conj = Pattern(
        "N1 I(and|as well as|besides) N2",
        from_id="N1",
        to_id="N2",
        indicator="I",
        link_type=LinkType.CONJ_AND,
    )
    pattern_abs = Pattern(
        "N1 BE I(kind of|class of) N2",
        "N1", "I", LinkType.ABSTRACT, "N2",
    )
    pattern_node = Pattern(
        "N",
        None, "N", LinkType.NODE, None,
    )
    pattern_if = Pattern("S1 I(if) S2", "S1", "I", "action", "S2")

    pattern_set_handler = PatternSetHandler([
        pattern_abs, pattern_if, pattern_action1, pattern_action2, pattern_attr, pattern_conj, pattern_node 
    ])

    test_cases = [
        (
            [
                Token("I", TokenTag.NOUN),
                Token("don't", TokenTag.ADV),
                Token("like", TokenTag.VERB),
                Token("and", TokenTag.CONJUNCTION),
                Token("love", TokenTag.VERB),
                Token("the", TokenTag.ARTICLE),
                Token("guy", TokenTag.NOUN),
                Token("writing", TokenTag.VERB),
            ],
            [
                MatchedPattern(pattern_action1, [
                    Token("I", TokenTag.NOUN),
                    Token("like", TokenTag.VERB),
                    Token("guy", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_action1, [
                    Token("I", TokenTag.NOUN),
                    Token("love", TokenTag.VERB),
                    Token("guy", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_action2, [
                    Token("I", TokenTag.NOUN),
                    Token("writing", TokenTag.VERB),
                ]),
                MatchedPattern(pattern_conj, [
                    Token("I", TokenTag.NOUN),
                    Token("and", TokenTag.CONJUNCTION),
                    Token("guy", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_node, [
                    Token("I", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_node, [
                    Token("guy", TokenTag.NOUN),
                ]),
            ],
        ),
        (
            [
                Token("I", TokenTag.NOUN),
                Token("could", TokenTag.VERB),
                Token("do", TokenTag.VERB),
                Token("if", TokenTag.ADV),
                Token("you", TokenTag.NOUN),
                Token("like", TokenTag.VERB),
            ],
            [
                MatchedPattern(pattern_if, [
                    [
                        MatchedPattern(pattern_action2, [
                        Token("I", TokenTag.NOUN),
                        Token("could", TokenTag.VERB),
                        ]),
                        MatchedPattern(pattern_action2, [
                            Token("I", TokenTag.NOUN),
                            Token("do", TokenTag.VERB),
                        ]),
                        MatchedPattern(pattern_node, [
                            Token("I", TokenTag.NOUN),
                        ]),
                    ],
                    Token("if", TokenTag.ADV),
                    [
                        MatchedPattern(pattern_action2, [
                            Token("you", TokenTag.NOUN),
                            Token("like", TokenTag.VERB),
                        ]),
                        MatchedPattern(pattern_node, [
                            Token("you", TokenTag.NOUN),
                        ]),
                    ],
                ])
            ],
        ),
        (
            [
                Token("Apple", TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Token("kind", TokenTag.NOUN),
                Token("of", TokenTag.PREPOSITION),
                Token("fruit", TokenTag.NOUN),
                Token(".", TokenTag.PUNCTUATION),
            ],
            [
                MatchedPattern(pattern_abs, [
                    Token("Apple", TokenTag.NOUN),
                    Token("is", TokenTag.VERB),
                    Phrase([
                        Token("kind", TokenTag.NOUN),
                        Token("of", TokenTag.PREPOSITION),
                    ]),
                    Token("fruit", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_node, [
                    Token("Apple", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_node, [
                    Token("fruit", TokenTag.NOUN),
                ]),
            ],
        ),
        (
            [
                Phrase([
                    Token("Red", TokenTag.ADJ),
                    Token("Apple", TokenTag.NOUN),
                ], TokenTag.NOUN),
                Token("is", TokenTag.VERB),
                Phrase([
                    Token("kind", TokenTag.NOUN),
                    Token("of", TokenTag.PREPOSITION),
                ]),
                Token("fruit", TokenTag.NOUN),
                Token(".", TokenTag.PUNCTUATION),
            ],
            [
                MatchedPattern(pattern_abs, [
                    Phrase([
                        Token("Red", TokenTag.ADJ),
                        Token("Apple", TokenTag.NOUN),
                    ], TokenTag.NOUN),
                    Token("is", TokenTag.VERB),
                    Phrase([
                        Token("kind", TokenTag.NOUN),
                        Token("of", TokenTag.PREPOSITION),
                    ]),
                    Token("fruit", TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_node, [
                    Phrase([
                        Token("Red", TokenTag.ADJ),
                        Token("Apple", TokenTag.NOUN),
                    ], TokenTag.NOUN),
                ]),
                MatchedPattern(pattern_node, [
                    Token("fruit", TokenTag.NOUN),
                ]),
            ],
        ),
        (
            [Token("Apple", TokenTag.NOUN)],
            [MatchedPattern(pattern_node, [Token("Apple", TokenTag.NOUN)])]
        ),
        (
            [
                Token("Apple", TokenTag.NOUN),
                Token("orange", TokenTag.NOUN)
            ],
            [
                MatchedPattern(pattern_node, [Token("Apple", TokenTag.NOUN)]),
                MatchedPattern(pattern_node, [Token("orange", TokenTag.NOUN)]),
            ]
        ),
        (
            [
                Token("Apple", TokenTag.NOUN),
                Token("lele", TokenTag.PREPOSITION),
                Token("orange", TokenTag.NOUN),
            ],
            [
                MatchedPattern(pattern_node, [Token("Apple", TokenTag.NOUN)]),
                MatchedPattern(pattern_node, [Token("orange", TokenTag.NOUN)]),
            ]
        ),
    ]

    for tokens, expected_matched_patterns in test_cases:
        before_tokens = [token for token in tokens]
        assert pattern_set_handler.match_tokens(tokens) == expected_matched_patterns
        assert tokens == before_tokens


def test_phrase_to_link():
    token_five = Token("five", TokenTag.NUMERAL)
    token_key = Token("key", TokenTag.ADJ)
    token_states = Token("states", TokenTag.NOUN)
    token_key_states = Phrase([token_key, token_states], TokenTag.NOUN)
    token_five_key_states = Phrase([token_five, token_key_states], TokenTag.NOUN)

    test_cases = [
        (
            token_five_key_states,
            [
                (token_five_key_states, token_key_states),
                (token_key_states, token_states)
            ]
        )
    ]

    ph = PatternSetHandler()
    for phrase, expected in test_cases:
        actual = ph._phrase_to_link(phrase)
        expected = [
            SemanticLink(SemanticNode(expected_from), SemanticNode(Token("")), LinkType.ABSTRACT, SemanticNode(expected_to))
            for expected_from, expected_to in expected
        ]

        assert actual == expected


def test_handler_match_sentence():
    ph = PatternSetHandler([
        Pattern("N1 BE I(kind of) N2", "N1", "I", "abstract", "N2"),
        Pattern("N1 V N2", "N1", "V", "action", "N2"),
        Pattern("N1 V", "N1", "V", "action", None),
        Pattern("S1 I(if) S2", "S1", "I", "condition", "S2"),
    ])

    test_cases = [
        (
            Sentence("Apple is a kind of fruit."),
            W_SLN([
                SemanticLink(
                    SemanticNode(Token("Apple", TokenTag.NOUN)),
                    SemanticNode(Phrase([
                        Token("kind", TokenTag.NOUN),
                        Token("of", TokenTag.PREPOSITION),
                    ])),
                    LinkType.ABSTRACT,
                    SemanticNode(Token("fruit", TokenTag.NOUN)),
                )
            ]),
        )
    ]

    for input_sentence, expected_wsln in test_cases:
        print(input_sentence)
        # assert ph.match_sentence(input_sentence) == expected_wsln


def test_pattern_set_handler_from_file_match_sentence(pattern_set_handler_from_file):
    assert len(pattern_set_handler_from_file.patterns) > 0

    test_cases = [
        (
            Sentence("If he wins five key states, Republican candidate Mitt Romney will be elected President in 2008."),
            [
                ("he", "If", LinkType.CONDITION, "he"),
                ("he", "wins", LinkType.ACTION, "five key states"),
                ("five key states", ",", LinkType.SEQUENTIAL, "Republican candidate Mitt Romney"),
                ("Republican candidate Mitt Romney", "will be elected", LinkType.ACTION, "President"),
                ("President", "in", LinkType.SITUATION, "2008"),
                ("five key states", "", LinkType.ABSTRACT, "key states"),
                ("key states", "", LinkType.ABSTRACT, "states"),
                ("Republican candidate Mitt Romney", "", LinkType.ABSTRACT, "candidate Mitt Romney"),
            ]
        ),
        # (
        #     Sentence("I will come with you if he likes."),
        #     []
        # ),
        # (
        #     Sentence("Apple is a kind of fruit."),
        #     [],
        # ),
    ]

    for sentence, expected_links in test_cases:
        w_sln = pattern_set_handler_from_file.match_sentence(sentence)

        assert len(w_sln.links) == len(expected_links)

        for link, (from_text, indicator_text, link_type, to_text) in zip(w_sln.links, expected_links):
            assert (
                link.from_node.token.text == from_text
                and link.indicator_node.token.text == indicator_text
                and link.link_type == link_type
                and link.to_node.token.text == to_text
            )


def test_wsln_search_incomplete_link():
    link_I_love_your_dog = SemanticLink(
        SemanticNode(Token("I")),
        SemanticNode(Token("love")),
        LinkType.ACTION,
        SemanticNode(Phrase([Token("your"), Token("dog")])),
    )
    link_I_am_good = SemanticLink(
        SemanticNode(Token("I")),
        SemanticNode(Token("am")),
        LinkType.ATTRIBUTE,
        SemanticNode(Token("good"))
    )
    link_I_and_dog = SemanticLink(
        SemanticNode(Token("I")),
        SemanticNode(Token("and")),
        LinkType.CONJ_AND,
        SemanticNode(Token("dog")),
    )
    link_dog_barking = SemanticLink(
        SemanticNode(Token("dog")),
        SemanticNode(Token("barking")),
        LinkType.ACTION,
        SemanticNode(Token("dog")),
    )

    test_cases = [
        (
            [
                link_I_love_your_dog,
                link_I_am_good,
                link_I_and_dog,
                link_dog_barking,
            ],
            [
                (
                    {
                        "from_node": SemanticNode(Token("I")),
                    },
                    [
                        link_I_love_your_dog,
                        link_I_am_good,
                        link_I_and_dog,
                    ]
                ),
                (
                    {
                        "link_type": LinkType.ACTION,
                    },
                    [
                        link_I_love_your_dog,
                        link_dog_barking,
                    ]
                ),
                (
                    {
                        "from_node": SemanticNode(Token("I")),
                        "to_node": SemanticNode(Token("dog")),
                    },
                    [
                        link_I_and_dog,
                    ]
                ),
                (
                    {
                        "to_node": SemanticNode(Phrase([Token("your"), Token("dog")])),
                    },
                    [
                        link_I_love_your_dog,
                    ]
                )
            ]
        ),
    ]

    for input_links, conditions in test_cases:
        w_sln = W_SLN(input_links) 
        for condition, expected_links in conditions:
            assert w_sln.search_incomplete_link(**condition) == expected_links