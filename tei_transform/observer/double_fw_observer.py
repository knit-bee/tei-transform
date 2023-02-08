from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class DoubleFwObserver(AbstractNodeObserver):
    """
    Observer for <fw/> elements with child and <fw/> parent.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "fw":
            parent = node.getparent()
            if (
                parent is not None
                and etree.QName(parent).localname == "fw"
                and list(node.iterchildren(["{*}list", "{*}fw"])) != []
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
