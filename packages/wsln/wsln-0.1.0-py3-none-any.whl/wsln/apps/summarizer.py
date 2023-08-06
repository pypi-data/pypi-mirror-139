# add parent path to python path
import sys
import nltk
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from wsln.settings import version, pattern_handler
from wsln.lexer import Document, Sentence
from wsln.parser import Pattern, PatternSetHandler, LinkType, W_SLN
from wsln.apps.datasets import read_paper_dataset, read_cnn_corpus, read_legal_corpus
from wsln.apps.word_scoring import smi
from tqdm import tqdm
from typing import Dict, List, Set


recorder = {}

def print_msg(query_link, query_sentence, sum, message: str):
    global recorder
    # print(query_link)
    # print(query_sentence)
    # print(sum)
    # print(message)
    # print("=========")
    # print()

    if message not in recorder:
        recorder[message] = 0
    recorder[message] += 1


class SentenceScore:

    def __init__(self, index: int, sentence: Sentence, w_sln: W_SLN, score: float, selected: bool) -> None:
        self.index = index
        self.sentence = sentence
        self.w_sln = w_sln
        self.score = score
        self.selected = selected

        self.meaningful_words = self._meaningful_words()

    def _meaningful_words(self) -> Set[str]:
        word_set = set()
        for link in self.w_sln.links:
            word_set |= set(
                link.from_node.token.text.split(" ")
                + link.to_node.token.text.split(" ")
                + (link.indicator_node.token.text.split(" ") if link.link_type in [LinkType.ACTION, LinkType.ATTRIBUTE] else [])
            )
        return word_set - {''}

    def evaluate_score(self, rank_dict):
        def get_word_score(word):
            if word not in rank_dict:
                print(word, "not occurred")
            return rank_dict.get(word, 0)

        self.score = sum(get_word_score(word) for word in self.meaningful_words)



def simplified(summary_wsln, sentence):
    pass


def summarize(rank_dict: Dict[str, float], document: Document, d_r: float = 0.5, simplified_proportion: float = 0.3, metric="censmi", desired_length = 150) -> str:
    assert 0 <= d_r < 1
    assert 0 <= simplified_proportion < 1

    sentence_score_tuples = [
        SentenceScore(index, sentence, pattern_handler.match_sentence(sentence), 0., False)
        for index, sentence in enumerate(document.sentences)
    ]

    doc_wsln = W_SLN()
    for score_tuple in sentence_score_tuples:
        doc_wsln += score_tuple.w_sln

    summary_wsln = W_SLN()
    summary = ""
    summary_tuples = []
    # TODO: 改成预期单词数量
    # for _ in range(10):
    while len(summary.split(" ")) < desired_length:
        
        for sentence_score_tuple in sentence_score_tuples:
            score = 0
            for link in sentence_score_tuple.w_sln.links:
                for word in sentence_score_tuple.meaningful_words:
                    if word not in rank_dict:
                        print(f"{word} not in rank_dict")
                    score += rank_dict.get(word, 0)
            # TODO: 乘系数
            sentence_score_tuple.score = score

        sorted_sentences = sorted(
            filter(lambda x: x.selected is False, sentence_score_tuples),
            key = lambda x: -x.score
        )

        if not sorted_sentences:
            break

        selected_tuple = sorted_sentences[0]
        summary_tuples.append(selected_tuple)

        selected_tuple.selected = True

        redun_threshold = sorted(rank_dict.values())[int(len(rank_dict) * 0.2)]

        # 简化句子
        # for index, s_tuple in enumerate(summary_tuples):
        as_well_as = abs_red = attr_same = sit_same = pur = False
        red_nodes = []
        red_node_mapper = []
        for link in selected_tuple.w_sln.links:
            # 判断是否冗余
            red = False
            for token in (tokens := [link.from_node.token, link.indicator_node.token, link.to_node.token]):
                if all([rank_dict[word] < redun_threshold for word in token.text.split(" ") if word]):
                    red = True
                else:
                    red = False
                    break
            if red:
                print_msg(link, selected_tuple.sentence.text, summary, "redundant")
                red_nodes.extend([
                    link.from_node.token, link.indicator_node.token, link.to_node.token
                ])

            for s_link in summary_wsln.links:
                if link == s_link:
                    pass

                # for node in [link.from_node, link.indicator_node, link.to_node]:
                #     if isinstance(node.token, Phrase):
                #         for node.token.tokens in summary_wsln.nodes:
                #             print()
                #     pass

                # 判断abstract链接
                if link.link_type == LinkType.ABSTRACT and link.from_node == s_link.from_node and not abs_red:
                    # 那么把所有from_node给换成和这个from_node
                    # 还是看两个abstract链接中的from_node是否有交集？
                    # link.from_node
                    print_msg(link, selected_tuple.sentence.text, summary, "abstract redundant")
                    abs_red = True
                    red_node_mapper.append(
                        (link.from_node.token, link.to_node.token)
                    )
                    break
                    
                elif "as well as" in selected_tuple.sentence.text and not as_well_as:
                    print_msg(link, selected_tuple.sentence.text, summary, "as well as")
                    as_well_as = True
                elif link.link_type in [LinkType.ATTRIBUTE, LinkType.SIMILAR, LinkType.OWN] and link.to_node == s_link.to_node and link.from_node == s_link.from_node and link.link_type == s_link.link_type and not attr_same:
                    print_msg(link, selected_tuple.sentence.text, summary, "attr,sim,own all same")
                    attr_same = True
                    red_nodes.append(link.to_node.token)
                    break
                elif link.link_type in [LinkType.SITUATION, LinkType.CONDITION, LinkType.TEMPORAL, LinkType.CAUSE_EFFECT, LinkType.MEANS, LinkType.PURPOSE] and link.to_node == s_link.to_node and link.link_type == s_link.link_type and not sit_same:
                    print_msg(link, selected_tuple.sentence.text, summary, "sit, cond, temp, cause, means, pur to_node is same")
                    sit_same = True
                    red_nodes.append(link.to_node.token)
                    break
                # elif link.link_type in [LinkType.CONJ_AND, LinkType.CONJ_OR] and link.indicator_node.token.text == "as well as":
                #     print()
                elif link.link_type == LinkType.PURPOSE and link.indicator_node.token.text in ["aim to", "in order to", "want to", "would like to", "intend to"] and not pur:
                    print_msg(link, selected_tuple.sentence.text, summary, "pur is complex")
                    pur = True
                    red_nodes.append(link.to_node.token)
                    break
        
        if simplified_proportion:

            simplified = ""
            for token in selected_tuple.sentence.tokens:
                if token in red_nodes:
                    # print(token)
                    # print(token)
                    # simplified += token.text + " "
                    pass
                else:
                    for (ori_token, to_token) in red_node_mapper:
                        if token == ori_token:
                            # simplified += to_token.text + " "
                            break
                    else:
                        simplified += token.text + " "
            summary += simplified + ". "
        else:
            summary += selected_tuple.sentence.text

        summary_wsln += selected_tuple.w_sln
        # summary = " ".join([s.sentence.text for s in summary_tuples])

        if d_r:
            for word in selected_tuple.meaningful_words:
                rank_dict[word] *= d_r
                for c_word in doc_wsln.get_connected_tokens(word):
                    if c_word not in selected_tuple.meaningful_words:
                        rank_dict[word] /= d_r

    return summary


def rouge_score(reference, hypothesis):
    """
    reference: truth
    hypothesis: summary

    return: {
        "rouge-1": {"p": 1.0, "r": 1.0, "f": s}
        "rouge-2": ...,
        "rouge-l": ...,
    }
    """
    from rouge import Rouge
    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)
    return scores[0]


def statistics_link_in_summary(inputs):
    stat = {
        "summary": {},
        "text": {},
    }
    for abstract_sentences, text_sentences in inputs:
        for sentence in abstract_sentences:
            for link in pattern_handler.match_sentence(sentence).links:
                stat["summary"][link.link_type] = stat["summary"].get(link.link_type, 0) + 1

        for sentence in text_sentences:
            for link in pattern_handler.match_sentence(sentence).links:
                stat["text"][link.link_type] = stat["text"].get(link.link_type, 0) + 1

    print(stat)


def stat_main():
    statistics_link_in_summary((Document(abstract).sentences, Document(important + unimportant).sentences) for index, (abstract, important, unimportant) in enumerate(read_paper_dataset(), 1))
    statistics_link_in_summary((Document(abstract).sentences, Document(important + unimportant).sentences) for index, (abstract, important, unimportant) in enumerate(read_cnn_corpus(10000), 1))


if __name__ == "__main__":
    # stat_main()
    # exit()

    summarys = []
    abstracts = []

    def get_params():
        import itertools
        keys = ["d_r", "desired_length", "simplified_proportion"]
        values = [[0, 0.3], [120, 150], [0, 0.1, 0.2]]
        for value_list in itertools.product(*values):
            yield dict(zip(keys, value_list))

    score_recorder = []

    data = read_legal_corpus(500)
    # data = read_cnn_corpus(500)
    # data = list(read_paper_dataset())

    # for index, (abstract, important, unimportant) in enumerate(read_paper_dataset(), 1):
    # for index, (abstract, important, unimportant) in enumerate(read_cnn_corpus(500), 1):
    for index, (abstract, important, unimportant) in tqdm(enumerate(data, 1), total=len(data)):
        important = important.replace(".", ". ")
        unimportant = unimportant.replace(".", ". ")

        important_tokens = []
        # for sentence in nltk.sent_tokenize(important):
        for sentence in Document(important).sentences:
            important_tokens.extend([
                token.text for token in sentence.flatten()
            ])

        detailed_tokens = []
        # for sentence in nltk.sent_tokenize(unimportant):
        for sentence in Document(unimportant).sentences:
            detailed_tokens.extend([
                token.text for token in sentence.flatten()
            ])

        rank_dict = smi(important_tokens, detailed_tokens)
        wo_summary = summarize(rank_dict, Document(important) + Document(unimportant), d_r=0.7, simplified_proportion=0, desired_length=120)

        # summarys.append(nltk.sent_tokenize(summary))
        # abstracts.append(nltk.sent_tokenize(abstract))

        # wo_op_score = rouge_score(abstract, wo_summary)

        # rank_dict = smi(important_tokens, detailed_tokens)
        # w_summary = summarize(rank_dict, Document(important) + Document(unimportant), d_r=0.7, simplified_proportion=0.2, desired_length=120)

        # w_op_score = rouge_score(abstract, w_summary)

        # print(w_op_score['rouge-1']['f'] - wo_op_score['rouge-1']['f'])

        # print(w_summary)
        # print(wo_summary)
        # print("=======")

        # if w_op_score['rouge-1']['f'] - wo_op_score['rouge-1']['f'] > 0.15:
        #     print(w_summary)
        #     print(wo_summary)

        # summarys.append(nltk.sent_tokenize(summary))
        # abstracts.append(nltk.sent_tokenize(abstract))


    from metrics import rouge_perl
    # score = rouge_perl(abstracts, summarys, "test")
    # print(score)

    # score_recorder.append((params, score))

    print(recorder)
    print(score_recorder)

    exit()