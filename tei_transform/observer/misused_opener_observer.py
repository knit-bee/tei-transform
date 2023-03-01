from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class MisusedOpenerObserver(AbstractNodeObserver):
    """
    Observer for <opener/> elements not placed at the top of a section.

    Find <opener/> elements that have invalid older siblings and no
    children and change their tag to <ab/>.
    """

    def observe(self, node: etree._Element) -> bool:
        tags_allowed_before = {
            "argument",
            "byline",
            "dateline",
            "docDate",
            "docAuthor",
            "epigraph",
            "signed",
            "meeting",
            "head",
            "salute",
            "fw",
            "opener",
        }
        if (
            etree.QName(node).localname == "opener"
            and len(node) == 0
            and etree.QName(node.getparent()).localname != "list"
        ):
            invalid_sibling_before = [
                sibling
                for sibling in node.itersiblings(preceding=True)
                if etree.QName(sibling).localname not in tags_allowed_before
            ]
            if invalid_sibling_before != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "ab")
