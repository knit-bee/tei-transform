from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import change_element_tag


class MisusedBylineObserver(AbstractNodeObserver):
    """
    Observer for <byline/> elements that appear in the middle of <div/>.

    Find <byline/> elements that have older siblings with <p/> or <ab/>
    tags AND younger siblings with <p/>, <ab/>, or <head/> and change
    their tag to <ab/>.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "byline":
            if (
                list(node.itersiblings(["{*}p", "{*}ab"], preceding=True)) != []
                and list(node.itersiblings(["{*}p", "{*}ab", "{*}head"])) != []
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        change_element_tag(node, "ab")
