from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class InvalidRoleObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <div/> with @role attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname in {"div", "p"}
            and node.attrib.get("role") is not None
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
