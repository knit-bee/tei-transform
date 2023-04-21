import logging
from typing import Dict, Optional, Set

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element

logger = logging.getLogger(__name__)


class PParentObserver(AbstractNodeObserver):
    """
    Observer for elements that have <div/> as parent instead of <p/>.

    Find elements with <div/> parent and add an intermediate <p/> as
    parent that is inserted at the index of the target element.
    This requires configuration by setting the target elements that
    should be handled.
    """

    def __init__(self, target_elems: Optional[Set[str]] = None) -> None:
        self.config_required: bool = True
        self.target_elems = target_elems

    def observe(self, node: etree._Element) -> bool:
        if (
            self.target_elems is not None
            and etree.QName(node).localname in self.target_elems
        ):
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in {"div", "body"}:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        new_p = create_new_element(node, "p")
        parent = node.getparent()
        node_index = parent.index(node)
        parent.insert(node_index, new_p)
        new_p.append(node)

    def configure(self, config_dict: Dict[str, str]) -> None:
        target_elems = config_dict.get("target")
        if not target_elems:
            logger.warning("Invalid configuration for PParentObserver")
            return
        self.target_elems = {elem.strip() for elem in target_elems.split(",")}
