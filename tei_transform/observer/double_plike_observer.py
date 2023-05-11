import logging
from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import merge_into_parent

logger = logging.getLogger(__name__)


class DoublePlikeObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <ab/> elements with parent <p/> or <ab/>.

    Find <p/> and <ab/> elements that have <p/> or <ab/> as parent
    and strip the inner tag (text and tail as well as the children
    of the inner element will be preserved).
    This observer can be configured to insert an <lb/> element to
    separate text parts of target and parent resp. older sibling.
    """

    def __init__(self, action: Optional[str] = None) -> None:
        self.action = action

    def observe(self, node: etree._Element) -> bool:
        p_like_tags = {"p", "ab"}
        if etree.QName(node).localname in p_like_tags:
            parent = node.getparent()
            if parent is not None and etree.QName(parent).localname in p_like_tags:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        add_lb = False
        if self.action == "add-lb":
            add_lb = True
        merge_into_parent(node, add_lb=add_lb)

    def configure(self, config_dict: Dict[str, str]) -> None:
        action = config_dict.get("action", None)
        if action is not None:
            self.action = action
        else:
            logger.warning("Invalid configuration, using default.")
