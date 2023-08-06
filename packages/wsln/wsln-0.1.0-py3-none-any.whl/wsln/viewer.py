
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

from wsln.lexer import Document
from wsln.parser import W_SLN

def view_sln_of_html(sln):
    pass

def view_sln_of_jpg(sln):
    pass

def view_sln_of_neo4j_statements(wsln: W_SLN):
    def _get_node_hash(text):
        return text.replace(" ", "_").replace("-", "_")
        
    def _get_link_hash(link):
        string = f"{link.link_name}_{_get_node_hash(link.literal)}"
        for appendix in link.appendix_links:
            string += f"_{appendix.link_name}_{_get_node_hash(appendix.literal)}"
        
        return string

    node_stats_set, link_stats_set = set(), set()
    for link in wsln.links:
        node_tag = "NODE"

        from_node_hash = _get_node_hash(link.from_node.text)
        to_node_hash = _get_node_hash(link.to_node.text)

        if from_node_hash:
            node_stats_set.add(
                f"CREATE ({from_node_hash}:{node_tag} {{name: '{link.from_node.text}'}})"
            )
        if to_node_hash:
            node_stats_set.add(
                f"CREATE ({to_node_hash}:{node_tag} {{name: '{link.to_node.text}'}})"
            )

        from_node_hash = from_node_hash or to_node_hash
        to_node_hash = to_node_hash or from_node_hash

        if len(link.indicator_node.text) <= 1:
            if to_node_hash in from_node_hash or from_node_hash in to_node_hash and from_node_hash != to_node_hash:
                link_text = "part_of"
            else:
                link_text = "co_occur"
        else:
            link_text = link.indicator_node.text
        link_stats_set.add(
            f"CREATE ({from_node_hash})-[:{_get_node_hash(link_text)}]->({to_node_hash})"
        )

    return list(node_stats_set) + list(link_stats_set)


if __name__ == "__main__":
    test_text = "Many approaches have been proposed previously to improve sentiment analysis on Twitter data. Even though some local contextual features could be help-ful to distinguish the two cases above, they still may not be enough to get the sentiment on the whole message correct. We established a state-of-the-art baseline that utilizes a variety of features, and built a topic-based sentiment mixture model with topic-specific Twitter data, all integrated in a semi-supervised training framework. We conduct pre-processing by removing stop words and some of the frequent words found in Twitter data. We intro-duce a topic-based mixture model for Twitter senti-ment. This motivates us to explore topic information explicitly in the task of sentiment analysis on Twitter data. This provides an opportunity for cross-domain topic identification when data from certain domain is more difficult to obtain than others. Lexi-cons with positive and negative words are important to sentiment classification."


    from wsln.settings import version, pattern_handler
    from wsln.lexer import Sentence

    wsln = W_SLN()
    
    for sentence in Document(test_text).sentences:
        wsln += pattern_handler.match_sentence(sentence)

    statements = view_sln_of_neo4j_statements(wsln)

    from pathlib import Path
    Path("./statements.txt").write_text("\n".join(statements))
    
    