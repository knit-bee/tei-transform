from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MisusedBylineObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "byline":
            if (
                list(node.itersiblings(["{*}p", "{*}ab"], preceding=True)) != []
                and list(node.itersiblings(["{*}p", "{*}ab", "{*}head"])) != []
            ):
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass
