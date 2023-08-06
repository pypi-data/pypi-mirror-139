import re
from collections import Counter, namedtuple
from enum import Enum
import string
import nltk
from typing import List, Union

symbols = r"！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."
symbols += string.punctuation + "\\"
symbols += "".join([chr(i) for i in range(945, 970)])
digits = "1234567890"


class TokenTag(Enum):
    DEFAULT = 0
    
    NOUN = 1
    VERB = 2
    ADV = 4
    ADJ = 5
    ARTICLE = 6
    CONJUNCTION = 7
    NUMERAL = 8

    PRONOUN = 9
    PREPOSITION = 10

    INDICATOR = 10

    PLACEHOLDER = 11

    INTERJECTION = 12

    WH_WORD = 13

    PUNCTUATION = 15

    ANY = 999


def nltk_pos_to_token_tag(pos_tag: str) -> TokenTag:
    mapper = {
        "CC": TokenTag.CONJUNCTION,
        "CD": TokenTag.NUMERAL,
        "DT": TokenTag.ARTICLE,
        "EX": TokenTag.PRONOUN,
        "FW": TokenTag.NOUN,
        "IN": TokenTag.PREPOSITION,
        "JJ": TokenTag.ADJ,
        "JJR": TokenTag.ADJ,
        "JJS": TokenTag.ADJ,
        "LS": TokenTag.ARTICLE,
        "MD": TokenTag.VERB,
        "NN": TokenTag.NOUN,
        "NNS": TokenTag.NOUN,
        "NNP": TokenTag.NOUN,
        "NNPS": TokenTag.NOUN,
        "PDT": TokenTag.ADJ,
        "POS": TokenTag.PLACEHOLDER,
        "PRP": TokenTag.NOUN,
        "PRP$": TokenTag.ADJ,
        "RB": TokenTag.ADV,
        "RBR": TokenTag.ADV,
        "RBS": TokenTag.ADV,
        "RP": TokenTag.PREPOSITION,
        "SYM": TokenTag.PLACEHOLDER,
        "TO": TokenTag.PREPOSITION,
        "UH": TokenTag.INTERJECTION,
        "VB": TokenTag.VERB,
        "VBD": TokenTag.VERB,
        "VBG": TokenTag.VERB,
        "VBN": TokenTag.VERB,
        "VBP": TokenTag.VERB,
        "VBZ": TokenTag.VERB,
        "WDT": TokenTag.WH_WORD,
        "WP": TokenTag.WH_WORD,
        "WP$": TokenTag.WH_WORD,
        "WRB": TokenTag.WH_WORD,
    }

    return mapper.get(pos_tag, TokenTag.PUNCTUATION)


class PhraseTag:

    ADJ_ADV = 1


class Tense:
    DEFAULT = 0

    PRESENT = 1


class Token:

    text: str
    token_tag: TokenTag
    
    def __init__(self, text, token_tag = TokenTag.DEFAULT):
        self.text = text
        self.token_tag = token_tag

    @property
    def is_ordinal(self):
        return (
            self.text in ["first", "second", "third"] or 
            ((self.token_tag in [TokenTag.ADJ, TokenTag.NUMERAL]) and self.text.endswith("th"))
        )

    def flatten(self):
        return [self]

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.text == other.text and self.token_tag == other.token_tag
        return False
    
    def __repr__(self):
        return f"Token({self.text}, {self.token_tag})"

    def __hash__(self):
        return hash(repr(self))

NULL_TOKEN = Token("", TokenTag.ANY)


class Phrase(Token):

    def __init__(self, tokens: List[Token], token_tag: TokenTag = TokenTag.DEFAULT) -> None:
        self.tokens = tokens
        if not isinstance(token_tag, TokenTag):
            raise Exception(f"invalid token_tag: {token_tag}")
        self.token_tag = token_tag

    @property
    def text(self) -> str:
        return " ".join(to.text for to in self.tokens)

    def append(self, token: Token) ->  None:
        self.tokens.append(token)

    def flatten(self) -> List[Token]:
        flatten_tokens = []
        for token in self.tokens:
            if isinstance(token, Phrase):
                flatten_tokens.extend(token.flatten())
            else:
                flatten_tokens.append(token)
        return flatten_tokens

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, index):
        if isinstance(index, (int, slice)):
            return self.tokens[index]

        raise Exception("the index must be a int or slice")

    def __iter__(self):
        return iter(self.tokens)

    def __repr__(self):
        return f"Phrase({self.tokens}, {self.token_tag})"

    def __eq__(self, other):
        if isinstance(other, Phrase):
            if len(self) != len(other):
                return False
            
            return all(token == otoken for token, otoken in zip(self, other)) and self.token_tag == other.token_tag
        
        return False

    def __hash__(self):
        return hash(self.text)


def tokenize_text(text: str) -> List[Token]:
    import nltk
    words = nltk.word_tokenize(text)

    return Sentence([
        Token(word, nltk_pos_to_token_tag(pos_tag))
        for word, pos_tag in nltk.pos_tag(words)
    ])


def merge_same_tags(tokens: List[Token]) -> List[Token]:
    merged_tokens = []
    curr_token = tokens[0]

    for index in range(1, len(tokens)):
        next_token = tokens[index]

        if curr_token.token_tag == next_token.token_tag and curr_token.token_tag != TokenTag.PUNCTUATION:
            if isinstance(curr_token, Phrase):
                curr_token.append(next_token)
            else:
                curr_token = Phrase([curr_token, next_token], curr_token.token_tag)
        else:
            merged_tokens.append(curr_token)
            curr_token = next_token
    else:
        merged_tokens.append(curr_token)
    
    return merged_tokens


PhraseRule = namedtuple("PhraseRule", ["curr_token_tag", "next_token_tag", "token_tag"])

PHRASE_RULES = [
    PhraseRule(TokenTag.ADV, TokenTag.ADJ, TokenTag.ADJ),
    PhraseRule(TokenTag.ADJ, TokenTag.NOUN, TokenTag.NOUN),
    PhraseRule(TokenTag.NUMERAL, TokenTag.NOUN, TokenTag.NOUN), # six days
    PhraseRule(TokenTag.VERB, TokenTag.ADV, TokenTag.VERB),
    PhraseRule(TokenTag.ADV, TokenTag.VERB, TokenTag.VERB),
    PhraseRule(TokenTag.NOUN, TokenTag.ADV, TokenTag.NOUN),
]


def merge_by_phrase_rule(tokens: List[Token], phrase_rules) -> List[Token]:
    """TODO: nominate the core word

    Args:
        tokens (List[Token]): [description]
        phrase_rules ([type]): [description]

    Returns:
        [type]: [description]
    """
    merged_tokens = []

    index = 0
    while index < len(tokens) - 1:
        curr_token, next_token = tokens[index], tokens[index + 1]

        for phrase_rule in phrase_rules:
            if (curr_token.token_tag == phrase_rule.curr_token_tag and
                next_token.token_tag == phrase_rule.next_token_tag):
                merged_tokens.append(Phrase(
                    [curr_token, next_token], phrase_rule.token_tag
                ))
                index += 2
                break
        else:
            merged_tokens.append(curr_token)
            index += 1
    
    if index == len(tokens) - 1:
        merged_tokens.append(tokens[index])

    # until no new phrase can be merged
    if len(merged_tokens) != len(tokens):
        return merge_by_phrase_rule(merged_tokens, phrase_rules)

    return merged_tokens


class Sentence:

    def __init__(self, input: Union[List[Token], str]):
        if isinstance(input, str):
            text = input
            tokens = tokenize_text(text)
            tokens = merge_same_tags(tokens)
            tokens = merge_by_phrase_rule(tokens, PHRASE_RULES)
        elif isinstance(input, list):
            tokens = input
            # tokens = merge_same_tags(tokens)
            # tokens = merge_by_phrase_rule(tokens, PHRASE_RULES)
            text = ""
        else:
            raise Exception(f"unknown input {input}")

        self.text = text
        self.tokens = tokens

    def flatten(self) -> List[Token]:
        flatten_tokens = []
        for token in self.tokens:
            if isinstance(token, Phrase):
                flatten_tokens.extend(token.flatten())
            else:
                flatten_tokens.append(token)
        return flatten_tokens


    @property
    def noun_snippets(self):
        previous_noun_index = 0
        snippets = []

        for token_index, token in enumerate(self.tokens):
            if token.token_tag == TokenTag.NOUN and (token_index != 0 and token_index != len(self.tokens) - 1):
                snippets.append(self.tokens[previous_noun_index:token_index+1])
                previous_noun_index = token_index
        else:
            snippets.append(self.tokens[previous_noun_index:])

        return snippets
    
    def __getitem__(self, index):
        if isinstance(index, (int, slice)):
            return self.tokens[index]

        raise Exception("the index must be a int or slice")

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)

    def __eq__(self, other):
        if isinstance(other, Sentence):
            return self.tokens == other.tokens
        
        return False

    def __next__(self):
        pass
    
    def __repr__(self):
        return "Sentence([" + ", ".join(str(token) for token in self.tokens) + "])"


def segment_sentences(text: str):
    import nltk

    for char in string.punctuation:
        if char in text:
            text = text.replace(char, f" {char} ")

    text = " ".join(text.split())

    return nltk.sent_tokenize(text)


class Document:

    def __init__(self, text: str, coref : bool = False):
        if coref:
            # TODO
            import spacy
            nlp = spacy.load('en_core_web_sm')
            import neuralcoref
            neuralcoref.add_to_pipe(nlp, greedyness=0.1)
            #greedyness默认是0.5，值越大提取到的coreference 越多，当然噪音越多。
            doc = nlp('My sister has a dog. She loves him.')
            print(doc._.has_coref)
            print(doc._.coref_clusters)
            raise NotImplementedError("coref")

        self.sentences = [
            Sentence(sentence) for sentence in nltk.sent_tokenize(text)
            # Sentence(sentence) for sentence in segment_sentences(text)
        ]

    def __add__(self, other):
        self.sentences.extend(other.sentences)
        return self


def segment_sentences(text) -> List[str]:
    import nltk

    for char in string.punctuation:
        if char in text:
            text = text.replace(char, f" {char} ")

    text = " ".join(text.split())

    return nltk.sent_tokenize(text)