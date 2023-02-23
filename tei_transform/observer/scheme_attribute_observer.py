from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class SchemeAttributeObserver(AbstractNodeObserver):
    """
    Observer for @scheme attribute with empty value.

    Find elements with @scheme attribute that has only an empty string
    as value and remove the attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if node.attrib.get("scheme", None) == "":
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
