from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class HiWithWrongParentObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "hi":
            if etree.QName(node.getparent()).localname in {
                "body",
                "div",
                "div1",
                "div2",
                "div3",
                "div4",
                "div5",
                "div6",
                "div7",
            }:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
