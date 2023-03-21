from typing import Dict, List, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class PParentObserver(AbstractNodeObserver):
    def __init__(self, target_elems: Optional[List[str]] = None) -> None:
        self.config_required: bool = True
        self.target_elems = target_elems

    def observe(self, node: etree._Element) -> bool:
        if (
            self.target_elems is not None
            and etree.QName(node).localname in self.target_elems
        ):
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname == "div":
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass

    def configure(self, config_dict: Dict[str, str]) -> None:
        pass
