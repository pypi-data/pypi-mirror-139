import re
from collections import namedtuple
from enum import Enum
from pathlib import Path
from typing import Union, Optional, List, Any, Tuple
from wsln.lexer import Sentence, Token, TokenTag, Phrase
from wsln.utils import load_json_to_meta

class Operand(Enum):
    
    NOUN = 1
    VERB = 2
    BE = 3
    ADJ = 4
    ADV = 5

    SLN = 6

    INDICATOR = 10


symbol_defs = {
    "N": (TokenTag.NOUN, []),
    "V": (TokenTag.VERB, []),
    "BE": (TokenTag.ANY, ["be", "is", "am", "are", "were", "was"]),
    "ADJ": (TokenTag.ADJ, []),
    "ADV": (TokenTag.ADV, []),
    "I": (TokenTag.ANY, []),
    "NUM": (TokenTag.NUMERAL, []),
    "S": (TokenTag.ANY, []),
}


class Symbol:

    def __init__(self, identifier, candidates : Optional[List[str]] = None) -> None:
        if not identifier:
            self.identifier = identifier
            self.token_tag = TokenTag.DEFAULT
            self.candidates = []
            return

        result = re.search(r"([A-Z]+)(\d*)", identifier)
        label, index = result.group(1), result.group(2)

        if not label in symbol_defs:
            raise Exception(f"unknown identifier `{identifier}`")

        token_tag, word_list = symbol_defs[label]
        candidates = (candidates if candidates else []) + word_list

        self.identifier = identifier
        self.label = label
        self.index = index
        self.token_tag = token_tag
        self.candidates = candidates

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.identifier == other.identifier
        
        return False
    
    def __repr__(self):
        return f"Symbol({self.identifier}, {self.candidates})"

    def is_recursive(self):
        return self.label == "S"

    def match_tokens(self, tokens) -> int:
        if not self.candidates:
            return 1 if self.token_tag == tokens[0].token_tag else 0

        offsets = []
        prefix = ""

        # TODO: 可以提前终止，或者换Trie树
        for offset, token in enumerate(tokens, 1):
            prefix = ((prefix + " ") if prefix else "") + token.text

            for word in self.candidates:
                if word == prefix:
                    offsets.append(offset)
                    break

        return offsets[-1] if len(offsets) != 0 else 0


class LinkType(Enum):

    ACTION = 1
    ATTRIBUTE = 2
    NEGATIVE = 3

    SEQUENTIAL = 4
    CONJ_AND = 5
    CONJ_OR = 5.5
    SITUATION = 6
    CONDITION = 7
    CAUSE_EFFECT = 8
    ABSTRACT = 9
    PART_WHOLE = 9.5
    PURPOSE = 10
    SIMILAR = 11
    MEANS = 12
    OWN = 13

    TEMPORAL = 14

    NODE = 20

    # CO_OCCUR = 15


link_type_mapper = {
    "action": LinkType.ACTION,
    "attribute": LinkType.ATTRIBUTE,
    "negative": LinkType.NEGATIVE,
    "sequential": LinkType.SEQUENTIAL,
    "conj-and": LinkType.CONJ_AND,
    "conj-or": LinkType.CONJ_OR,
    "situation": LinkType.SITUATION,
    "condition": LinkType.CONDITION,
    "cause-effect": LinkType.CAUSE_EFFECT,
    "abstract": LinkType.ABSTRACT,
    "part-whole": LinkType.PART_WHOLE,
    "purpose": LinkType.PURPOSE,
    "similar": LinkType.SIMILAR,
    "means": LinkType.MEANS,
    "own": LinkType.OWN,
    "temporal": LinkType.TEMPORAL,
    "node": LinkType.NODE,
}


class SemanticNode:

    def __init__(self, content: Any) -> None:
        self.content = content

    @property
    def token(self) -> Optional[Token]:
        if isinstance(self.content, Token):
            return self.content
        return None

    @property
    def links(self) -> Optional[List[Token]]:
        if isinstance(self.content, list):
            return self.content
        return None

    @property
    def text(self) -> str:
        if self.token:
            return self.token.text
        if self.links:
            return ", ".join(str(link) for link in self.links)

    def __eq__(self, other) -> bool:
        if isinstance(other, SemanticNode):
            return self.content == other.content
        return False

    def __repr__(self) -> str:
        return f"SemanticNode({self.content})"

NULL_NODE = SemanticNode(Token(""))


class SemanticLink:

    def __init__(self, from_node: SemanticNode, indicator_node: SemanticNode, link_type: LinkType, to_node: SemanticNode):
        self.from_node = from_node
        self.indicator_node = indicator_node
        self.link_type = link_type
        self.to_node = to_node

    def __eq__(self, other) -> bool:
        if isinstance(other, SemanticLink):
            return (
                self.from_node == other.from_node
                and self.indicator_node == other.indicator_node
                and self.link_type == other.link_type
                and self.to_node == other.to_node
            )
        return False

    def __str__(self) -> str:
        return f"{self.from_node.text}-({self.indicator_node.text}, {self.link_type})->{self.to_node.text}"

    def __repr__(self) -> str:
        return f"SemanticLink({self.from_node}, {self.indicator_node}, {self.link_type}, {self.to_node})"


class W_SLN:

    def __init__(self, links: Optional[List[SemanticLink]] = None) -> None:
        self.links = links if links else []
    
    def __add__(self, other):
        self.links.extend(other.links)
        return self

    def __str__(self):
        return ", ".join(str(link) for link in self.links)
     
    def __repr__(self):
        return ", ".join(str(link) for link in self.links)
    
    def get_connected_tokens(self, text: str) -> List[Token]:
        tokens = []
        for link in self.links:
            if text in link.from_node.token.text or text in link.indicator_node.token.text or text in link.to_node.token.text:
                # TODO: token set
                tokens.extend(
                    link.from_node.token.flatten() + link.indicator_node.token.flatten() + link.to_node.token.flatten()
                )
        return [
            token
            for token in tokens if token.text != ""
        ]

    def search_incomplete_link(self,
            from_node: Optional[SemanticNode] = None,
            indicator_node: Optional[SemanticNode] = None,
            link_type: Optional[LinkType] = None,
            to_node: Optional[SemanticNode] = None,):

        def is_equal(node: SemanticNode, expected_node):
            return not expected_node or node == expected_node
        
        matched_links = []
        for link in self.links:
            if (is_equal(link.from_node, from_node)
                and is_equal(link.indicator_node, indicator_node)
                and is_equal(link.link_type, link_type)
                and is_equal(link.to_node, to_node)):
                
                matched_links.append(link)
        return matched_links

    def get_centroid(self, node: SemanticNode) -> int:
        centroid = 0
        for link in self.links:
            if node in [link.from_node, link.indicator_node, link.to_node]:
                centroid += 1
        return centroid


class MatchedPattern:

    def __init__(self, pattern, tokens: List[Union[List, Token]]):
        assert len(tokens) == len(pattern.symbols)
        self.pattern = pattern
        self.tokens = tokens

        self.symbol_identifiers = [symbol.identifier for symbol in self.pattern.symbols]
    
    @property
    def from_token(self):
        if not self.pattern.from_id:
            return Token("")
        return self.tokens[
            self.symbol_identifiers.index(self.pattern.from_id)
        ]

    @property
    def indicator_token(self):
        if not self.pattern.indicator:
            return Token("")
        return self.tokens[
            self.symbol_identifiers.index(self.pattern.indicator)
        ]

    @property
    def to_token(self) -> Optional[Token]:
        if self.pattern.to_id:
            return self.tokens[
                self.symbol_identifiers.index(self.pattern.to_id)
            ]
        return Token("")
        return 

    def _to_node(self, token: Token) -> SemanticNode:
        if isinstance(token, Token):
            return SemanticNode(token)
        if isinstance(token, MatchedPattern):
            return SemanticNode(token.to_link())
        if isinstance(token, list):
            return SemanticNode([
                mp.to_link()
                for mp in token
            ])
        return NULL_NODE

    def to_link(self) -> SemanticLink:
        return SemanticLink(
            self._to_node(self.from_token),
            self._to_node(self.indicator_token),
            self.pattern.link_type,
            self._to_node(self.to_token),
        )
    
    def __eq__(self, other):
        return self.pattern == other.pattern and self.tokens == other.tokens
    
    def __repr__(self):
        return f"MP({self.tokens})"


class Pattern:

    def __init__(self, pattern: str, from_id: str, indicator: str, link_type: Union[str, LinkType], to_id: str) -> None:
        self.symbols = [
            self._item_to_symbol(item)
            for item in re.findall(r"(\w+\(.*\)|\w+)", pattern)
        ]
        
        self.pattern = pattern
        self.from_id = from_id
        self.indicator = indicator
        self.to_id = to_id

        if isinstance(link_type, str):
            if link_type not in link_type_mapper:
                raise Exception(f"unknown link type {link_type}")
            self.link_type = link_type_mapper[link_type]
        elif isinstance(link_type, LinkType):
            self.link_type = link_type

    def _item_to_symbol(self, item: str) -> Symbol:
        """[summary]

        Args:
            item (str): like "V", "I1(like|love)"

        Returns:
            [type]: [description]
        """
        result = re.search(r"(\w+)(\(.+\))*", item)

        identifier = result.group(1)
        if (candidates := result.group(2)) is not None:
            candidates = candidates[1:-1].split("|")
        
        return Symbol(identifier, candidates)

    def match_tokens(self, tokens: List[Token]) -> List[MatchedPattern]:
        matched_patterns = []
        for sequence in self._match_tokens(self.symbols, tokens):
            symbols = [item[0] for item in sequence]
            tokens = [item[1] for item in sequence]

            if len(symbols) == len(self.symbols):
                matched_patterns.append(
                    MatchedPattern(self, tokens)
                )
        return matched_patterns

    def _find_all_matched_indexes(self, symbol, tokens) -> List[int]:
        indexes = []
        for token_index, token in enumerate(tokens):
            if (offset := symbol.match_tokens(tokens[token_index:])) != 0:
                indexes.append((token_index, offset))
        return indexes

    
    # TODO: 需要好好测试这个函数，太复杂了
    def _match_tokens(self, pend_symbols: List[Symbol], tokens: List[Token]) -> List[Tuple[Symbol, Token]]:
        matched_sequences = []
        first_symbol = pend_symbols[0]

        if first_symbol.is_recursive():
            if len(pend_symbols) == 1:
                candidate_sequences = [[(first_symbol, tokens)]]
            else:
                # 预留一个单词给match_offset
                candidate_sequences = []
                for match_offset, extra_offset in self._find_all_matched_indexes(pend_symbols[1], tokens[1:]):
                    matched_tokens = tokens[:match_offset + 1]
                    second_tokens = tokens[match_offset + 1: match_offset + 1 + extra_offset]

                    if extra_offset == 1:
                        second_tokens = second_tokens[0]
                    else:
                        second_tokens = Phrase(second_tokens)

                    candidate_sequences += [
                        [(first_symbol, matched_tokens), (pend_symbols[1], second_tokens)] + matched_sequence
                        for matched_sequence in self._match_tokens(pend_symbols[2:], tokens[match_offset + 1 + extra_offset:])
                    ]
            return candidate_sequences

        for token_index, token in enumerate(tokens):
            # TODO: 如果是phrase级别的匹配，怎么办。
            # 如果已经按照规则合并以后，那就是一个text object，句子与symbol的匹配应该按照text object来
            # Verb(does) ADV(not) 和 I(never|does not)之间的匹配比较麻烦
            # token phrase token 之间的匹配，以整个text object为单位
            if first_symbol.is_recursive():
                pass
            else:
                match_offset = first_symbol.match_tokens(tokens[token_index:])

                if match_offset == 0:
                    continue
                # TODO: 简化
                matched_tokens = tokens[token_index: token_index + match_offset]

                if match_offset == 1:
                    matched_tokens = matched_tokens[0]
                else:
                    matched_tokens = Phrase(tokens[token_index: token_index + match_offset])

                if len(pend_symbols) == 1:
                    candidate_sequences = [[(first_symbol, matched_tokens)]]
                else:
                    candidate_sequences = [
                        [(first_symbol, matched_tokens)] + matched_sequence
                        for matched_sequence in self._match_tokens(pend_symbols[1:], tokens[token_index + match_offset:])
                    ]

            matched_sequences += candidate_sequences
        
        return matched_sequences

    def match_tokens_recursive(self, tokens, patterns):
        """
        目前解决
        S1 I(if) S2的情况

        TODO: 还没有考虑到
        N S1 S2 N的情况
        """
        t_index = s_index = 0
        while t_index < len(tokens) and s_index < len(self.symbols):
            symbol = self.symbols[s_index]

            # if symbol.is_recursive():
            #     if len

            if not symbol.is_recursive() and (offset := self.symbols[s_index].match_tokens(tokens[t_index:])) != 0:
                t_index += offset
                s_index += 1

                index_recorder.append((t_index, offset))
                break
            else:
                t_index += 1

        if s_index != len(non_recursive_symbols):
            return []
        
        # for 


        for pattern in self.pattern:
            pattern.match_tokens(token[:index])

        token[:index], token[index: index + offset], token[index+offset+1]
        

    def __eq__(self, other):
        return (
            self.pattern == other.pattern
            and self.from_id == other.from_id
            and self.indicator == other.indicator
            and self.to_id == other.to_id
            and self.link_type == other.link_type
        )

    def __str__(self) -> str:
        from_symbol = ind_symbol = to_symbol = None
        for symbol in self.symbols:
            if symbol.identifier == self.from_id:
                from_symbol = symbol
            if symbol.identifier == self.indicator:
                ind_symbol = symbol
            if symbol.identifier == self.to_id:
                to_symbol = symbol
        from_symbol = from_symbol if from_symbol else "%%"
        ind_symbol = ind_symbol if ind_symbol else "%%"
        to_symbol = to_symbol if to_symbol else "%%"
        return f"{from_symbol} -- {ind_symbol} --> {to_symbol}"


def match_pattern_greedy(symbols, sentence):
    """Return ONE matched pattern by greedy algorithm, but return a list

    if the match failed: return None
    else: return a list to indicate the tuple of token and symbol

    https://leetcode-cn.com/problems/is-subsequence/solution/pan-duan-zi-xu-lie-by-leetcode-solution/

    Steps:
        The sentence is REQUIRED contain at most two noun (phrase).

    To quickly match, prefilter the pattern match by its node (pod) count, more than
    """
    matched_sequence = []

    symbol_index = token_index = 0
    while symbol_index < len(symbols) and token_index < len(sentence):
        if symbols[symbol_index] == sentence[token_index]:
            matched_sequence.append(
                (symbols[symbol_index], sentence[token_index])
            )
            symbol_index += 1
        
        token_index += 1

    if symbol_index < len(symbols):
        return []

    return [matched_sequence]


class PatternSetHandler:

    def __init__(self, patterns: Optional[List[Pattern]] = None):
        self.patterns = patterns if patterns else []

    def append_patterns(self, patterns: List[Pattern]) -> None:
        for pattern in patterns:
            self.patterns.append(pattern)
    
    def read_patterns_from_file(self, file_path: Union[str, Path]) -> None:
        patterns_json = load_json_to_meta(file_path)

        for link in patterns_json.links:
            link_type = link.type
            for pattern in link.patterns:
                self.patterns.append(Pattern(
                    pattern.pattern,
                    pattern.from_id,
                    pattern.indicator if hasattr(pattern, "indicator") else None,
                    link_type,
                    pattern.to_id,
                ))
    
    # TODO: patterns需要被排序
    # 拥有更specific的需要放在前面，拥有递归的需要放前面
    # TODO: 如果
    def match_tokens(self, tokens: List[Token]) -> List[MatchedPattern]:
        _ts = tokens
        tokens = [token for token in tokens]
        matched_patterns = []
        for pattern in self.patterns:
            _mpatterns = pattern.match_tokens(tokens)
            for _mpattern in _mpatterns:

                for index, (symbol, token) in enumerate(zip(_mpattern.pattern.symbols, _mpattern.tokens)):

                    if symbol.is_recursive():
                        for t in token:
                            tokens.remove(t)
                        _mpattern.tokens[index] = self.match_tokens(_mpattern.tokens[index])
                        # matched_patterns.append(_mpattern)
                        recursive = True
                    elif token not in [_mpattern.from_token, _mpattern.to_token] and token in tokens:
                        tokens.remove(token)
                        # matched_patterns.append(_mpattern)
                        appended = True
                    elif token not in [_mpattern.from_token, _mpattern.to_token] and isinstance(token, Phrase):
                        for t in token:
                            if t in tokens:
                                tokens.remove(t)
                #         matched_patterns.append(_mpattern)
                    elif token not in [_mpattern.from_token, _mpattern.to_token]:
                        if isinstance(token, Token) and token not in tokens:
                            break
                        # if isinstance(token, Phrase):
                        #     for t in token:
                        #         print(t, tokens, t in tokens)
                        #         if t not in tokens:
                        #             break
                        #     else:
                        #         continue
                        #     break

                # if recursive and not appended:
                #     matched_patterns.append(_mpattern)

                # if (indicator := _mpattern.indicator_token) in tokens:
                #     tokens.remove(indicator)
                #     matched_patterns.append(_mpattern)
                # 如果这个symbol是递归的，那么就移除这些tokens
                # 如何确保移除的就是正确的token
                # 每个token内部都有一个索引编号
                # 那么如何判断相等呢？
                # 内容上相等和hash remove之间的关系，需要验证一下
                else:
                    matched_patterns.append(_mpattern)


        return matched_patterns

    def _phrase_to_link(self, token: Token) -> List[SemanticLink]:
        if isinstance(token, Phrase) and len(token) == 2 and token[0].token_tag != token[1].token_tag:
            return [SemanticLink(
                SemanticNode(token), 
                SemanticNode(Token("")),
                LinkType.ABSTRACT,
                SemanticNode(token[0] if token[0].token_tag == token.token_tag else token[1])
            )] + self._phrase_to_link(token[0]) + self._phrase_to_link(token[1])
        return []

    def match_sentence(self, sentence: Sentence) -> W_SLN:
        links = []
        for tokens in sentence.noun_snippets:
            links.extend([
                matched_pattern.to_link()
                for matched_pattern in self.match_tokens(tokens)
            ])

        for token in sentence.tokens:
            links += self._phrase_to_link(token)

        return W_SLN(links)