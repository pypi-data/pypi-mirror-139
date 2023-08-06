import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def phrase_rules():
    from wsln.lexer import PHRASE_RULES
    return PHRASE_RULES


@pytest.fixture(scope="session")
def pattern_set_handler_from_file():
    from wsln.parser import Pattern, PatternSetHandler, LinkType
    ph = PatternSetHandler()
    ph.read_patterns_from_file(Path(__file__).parent.parent / "patterns.json")

    return ph


@pytest.fixture(scope="session")
def pattern_set_handler():
    from wsln.parser import Pattern, PatternSetHandler, LinkType

    patterns = [
        Pattern(
            "N1 V N2",
            from_id="N1",
            indicator="V",
            to_id="N2",
            link_type=LinkType.ACTION,
        ),
        Pattern(
            "N1 V",
            from_id="N1",
            indicator="V",
            to_id="N1",
            link_type=LinkType.ACTION,
        ),
        Pattern(
            "N V ADJ",
            from_id="N",
            indicator="V",
            to_id="ADJ",
            link_type=LinkType.ATTRIBUTE,
        ),
        Pattern(
            "N1 I(and|as well as|besides) N2",
            from_id="N1",
            to_id="N2",
            indicator="I",
            link_type=LinkType.SEQUENTIAL_AND,
        ),
    ]

    return PatternSetHandler(patterns)


@pytest.fixture(scope="session")
def reason_rules():
    from wsln.builder import LinkType
    from wsln.reasoner import ReasonRule, PendLink

    return [
        ReasonRule(
            conditions=[
                PendLink("n1", "n2", LinkType.CAUSE_EFFECT, []),
                PendLink("n2", "n3", LinkType.CAUSE_EFFECT, []),
            ],
            outs=[
                PendLink("n1", "n3", LinkType.CAUSE_EFFECT, []),
            ],
        ),
        ReasonRule(
            conditions=[
                PendLink("n1", "n2", LinkType.ACTION, ["use"]),
                PendLink("n2", "n3", LinkType.ACTION, ["use", "use yes"]),
            ],
            outs=[
                PendLink("n1", "n3", LinkType.MEANS, []),
            ]
        ),
    ]