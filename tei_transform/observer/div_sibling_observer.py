from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class DivSiblingObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {"quote", "table"}:
            if list(node.itersiblings("{*}div", preceding=True)) != []:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
