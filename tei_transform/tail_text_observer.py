from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class TailTextObserver(AbstractNodeObserver):
    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname in {
            "p",
            "fw",
            "ab",
        }:
            if list(node.iterancestors("{*}text")) != []:
                if node.tail is not None and node.tail.strip():
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass


# add as plugin
# add integration test
