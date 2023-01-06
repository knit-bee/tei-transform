from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class HeadAfterPElementObserver(AbstractNodeObserver):
    """
    Observer for <head/> elements that have invalid elements as older siblings.

    Find <head/> elements after elements that are not <fw/> or part of
    model.divWrapper and change their tag to <ab/> and add the attribute
    [@type='head'].
    """

    def observe(self, node: etree._Element) -> bool:
        allowed_before = [  # mainly elements from model.divWrapper
            "fw",
            "opener",
            "argument",
            "byline",
            "dateline",
            "docAuthor",
            "docDate",
            "epigraph",
            "signed",
            "meeting",
            "salute",
        ]
        if etree.QName(node.tag).localname == "head":
            if [
                sibling
                for sibling in node.itersiblings(preceding=True)
                if etree.QName(sibling).localname not in allowed_before
            ] != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if (
            len(node) != 0
            or (node.text and node.text.strip())
            or (node.tail and node.tail.strip())
        ):
            change_element_tag(node, "ab")
            node.set("type", "head")
        else:
            node.getparent().remove(node)
