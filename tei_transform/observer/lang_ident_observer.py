from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class LangIdentObserver(AbstractNodeObserver):
    """
    Observer for <language/> that are missing @ident attribute.
    """

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "language"
            and node.attrib.get("ident", None) is None
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
