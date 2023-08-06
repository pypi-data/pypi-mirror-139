from wsln.parser import SemanticLink, SemanticNode, LinkType
from wsln.settings import template_handler
from collections import namedtuple
from itertools import permutations


class PendLink:

    def __init__(self, from_node: str, to_node: str, link_type, link_words):
        self.from_node = from_node
        self.to_node = to_node
        self.link_type = link_type
        self.link_words = link_words

class ResolvedLink:

    def __init__(self, from_node: SemanticNode, to_node: SemanticNode, link_type: LinkType, link_words: list):
        self.from_node = from_node
        self.to_node = to_node
        self.link_type = link_type
        self.link_words = link_words

    def __eq__(self, other):
        if isinstance(other, SemanticLink):
            link = other

            return (True if self.link_words == [] else link.indicator_token.literal  in self.link_words) and (
                self.from_node == link.from_node and
                self.to_node == link.to_node and
                self.link_type == link.link_type
            )
        elif isinstance(other, ResolvedLink):
            return (
                self.from_node == other.from_node and 
                self.to_node == other.to_node and
                self.link_type == other.link_type and
                self.link_words == other.link_words
            )
        
        return False
    
    def __repr__(self):
        return f"{self.from_node}-{self.link_type}({self.link_words})->{self.to_node}"


class ReasonRule:

    def __init__(self, conditions, outs):
        self.conditions = conditions
        self.outs = outs

    @property
    def node_indicator_set(self):
        indicator_set = set()
        for condition_link in self.conditions:
            indicator_set.update([condition_link.from_node, condition_link.to_node])
        return indicator_set

    def find_all_matched_links(self, sln):
        """brute force to find all matched conditional links
        
        Find all unique nodes, and match them

        Args:
            link_set ([type]): [description]

        Returns:
            [type]: [description]
        """

        all_matched_links = []
        all_derived_links = []

        for nodes in permutations(sln.nodes, len(self.node_indicator_set)):
            indicator_node_mapper = {
                indicator: node for node, indicator in zip(nodes, self.node_indicator_set)
            }

            matched_links = []

            for resolved_link in [
                ResolvedLink(
                    from_node=indicator_node_mapper[condition_link.from_node],
                    to_node=indicator_node_mapper[condition_link.to_node],
                    link_type=condition_link.link_type,
                    link_words=condition_link.link_words,
                ) for condition_link in self.conditions
            ]:
                for link in sln.links:
                    if resolved_link == link:
                        matched_links.append((
                            resolved_link,
                            link,
                        ))
                        break
                else:
                    break
            else:
                # successful matched conditions
                all_matched_links.append(matched_links)
                all_derived_links.append([
                    ResolvedLink(
                        from_node=indicator_node_mapper[out_link.from_node],
                        to_node=indicator_node_mapper[out_link.to_node],
                        link_type=out_link.link_type,
                        link_words=out_link.link_words,
                    ) for out_link in self.outs
                ])
        
        return all_matched_links, all_derived_links


def read_reasoning_rules_from_file():
    pass

    return [ReasonRule()]


def divide_link_community(communities):
    """divide the links into reasoning communities, 
    the initial communities are the links extracted from different sentences.

    Args:
        communities (list): a list of SLN, where the links are all in a community
    """
    new_communities = []

    for community in communities:
        for new_community in new_communities:
            # no identical link

            if len(community.links | new_community.links) != len(community.links) + len(new_community.links):
                new_community.update(community)
                break
        else:
            new_communities.append(community)

    if len(communities) == len(new_communities):
        return new_communities

    return divide_link_community(new_communities)


