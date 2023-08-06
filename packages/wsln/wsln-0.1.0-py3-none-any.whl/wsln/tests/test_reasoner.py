from wsln.lexer import Token, Phrase, TokenTag
from wsln.builder import W_SLN, SemanticLink, SemanticNode, LinkType
from wsln.reasoner import divide_link_community, ResolvedLink

def test_divide_link_community():
    link1 = SemanticLink(
                from_node=SemanticNode(Token("A", TokenTag.NOUN)),
                to_node=SemanticNode(Token("B", TokenTag.NOUN)),
                indicator_token=Phrase([
                    Token("as", TokenTag.PREPOSITION),
                    Token("well", TokenTag.ADV),
                    Token("as", TokenTag.PREPOSITION),
                ], TokenTag.ANY),
                link_type=LinkType.SEQUENTIAL_AND,
            )
    link2 = SemanticLink(
                from_node=SemanticNode(Token("B", TokenTag.NOUN)),
                to_node=SemanticNode(Token("good", TokenTag.ADJ)),
                indicator_token=Token("is", TokenTag.VERB),
                link_type=LinkType.ATTRIBUTE,
            )
    link3 = SemanticLink(
                from_node=SemanticNode(Token("A", TokenTag.NOUN)),
                to_node=SemanticNode(Token("B", TokenTag.NOUN)),
                indicator_token=Phrase([
                    Token("as", TokenTag.PREPOSITION),
                    Token("well", TokenTag.ADV),
                ], TokenTag.ANY),
                link_type=LinkType.SEQUENTIAL_AND,
            )
    link4 = SemanticLink(
                from_node=SemanticNode(Token("C", TokenTag.NOUN)),
                to_node=SemanticNode(Token("good", TokenTag.ADJ)),
                indicator_token=Token("is", TokenTag.VERB),
                link_type=LinkType.ATTRIBUTE,
            )
    link5 = SemanticLink(
                from_node=SemanticNode(Token("good", TokenTag.NOUN)),
                to_node=SemanticNode(Token("C", TokenTag.ADJ)),
                indicator_token=Token("is", TokenTag.VERB),
                link_type=LinkType.ATTRIBUTE,
            )
    

    test_cases = [
        (
            [
                {link1, link2},
                {link3},
                {link2, link4},
                {link5},
            ],
            [
                {link1, link2, link4},
                {link3},
                {link5},
            ],
        ),
        (
            [
                {link1, link2},
                {link3, link4},
                {link2, link4},
                {link5},
            ],
            [
                {link1, link2, link3, link4},
                {link5},
            ],
        ),
    ]

    for input_link_sets, expected_link_sets in test_cases:
        input_communities = [W_SLN(links=list(input_link_set)) for input_link_set in input_link_sets]
        communities = divide_link_community(input_communities)

        assert communities == [W_SLN(links=list(expected_link_set)) for expected_link_set in expected_link_sets]


def test_find_all_matched_links(reason_rules):
    # cause_effect_trans_rule, action_use_trans_rule = reason_rules

    car_node = SemanticNode(Token("car", TokenTag.NOUN))
    engine_node = SemanticNode(Token("engine", TokenTag.NOUN))
    gas_node = SemanticNode(Token("gas", TokenTag.NOUN))

    car_use_engine_link = SemanticLink(
        from_node=car_node,
        to_node=engine_node,
        link_type=LinkType.ACTION,
        indicator_token=(Token("use", TokenTag.VERB)),
    )

    engine_use_gas_link = SemanticLink(
        from_node=engine_node,
        to_node=gas_node,
        link_type=LinkType.ACTION,
        indicator_token=Phrase([Token("use", TokenTag.VERB), Token("yes", TokenTag.VERB)], TokenTag.VERB),
    )

    engine_use_no_gas_link = SemanticLink(
        from_node=engine_node,
        to_node=gas_node,
        link_type=LinkType.ACTION,
        indicator_token=Phrase([Token("use", TokenTag.VERB), Token("no", TokenTag.VERB)], TokenTag.VERB),
    )

    you_node = SemanticNode(Token("you", TokenTag.NOUN))
    leg_node = SemanticNode(Token("leg", TokenTag.NOUN))
    broken_node = SemanticNode(Token("broken", TokenTag.NOUN))

    you_cause_leg = SemanticLink(
        from_node=you_node,
        to_node=leg_node,
        link_type=LinkType.CAUSE_EFFECT,
        indicator_token=(Token("therefore", TokenTag.VERB)),
    )

    leg_cause_broken = SemanticLink(
        from_node=leg_node,
        to_node=broken_node,
        link_type=LinkType.CAUSE_EFFECT,
        indicator_token=(Token("therefore", TokenTag.VERB)),
    )

    test_cases = [
        (
            W_SLN(links=[
                car_use_engine_link,
                engine_use_gas_link,
            ]),
            [[
                (ResolvedLink(car_node, engine_node, LinkType.ACTION, ["use"]), car_use_engine_link),
                (ResolvedLink(engine_node, gas_node, LinkType.ACTION, ["use", "use yes"]), engine_use_gas_link),
            ]],
            [[
                ResolvedLink(car_node, gas_node, LinkType.MEANS, []),
            ]],
        ),
        (
            W_SLN(links=[
                you_cause_leg,
                leg_cause_broken,
                car_use_engine_link,
            ]),
            [[
                (ResolvedLink(you_node, leg_node, LinkType.CAUSE_EFFECT, []), you_cause_leg),
                (ResolvedLink(leg_node, broken_node, LinkType.CAUSE_EFFECT, []), leg_cause_broken),
            ]],
            [[
                ResolvedLink(you_node, broken_node, LinkType.CAUSE_EFFECT, [])
            ]],
        ),
        (
            W_SLN(links=[
                you_cause_leg,
                car_use_engine_link,
                engine_use_no_gas_link,
            ]),
            [],
            [],
        )
    ]

    for input_sln, expected_matched_links, expected_derived_links in test_cases:
        matched_links, derived_links = [], []
        for reason_rule in reason_rules:
            _matched, _derived = reason_rule.find_all_matched_links(input_sln)
            matched_links += _matched
            derived_links += _derived

        assert matched_links == expected_matched_links
        assert derived_links == expected_derived_links

