from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class PAsDivSiblingObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "p"
            and list(node.itersiblings("{*}div", preceding=True)) != []
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
