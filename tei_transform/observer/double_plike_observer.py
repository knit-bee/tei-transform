import logging
from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element, merge_into_parent

logger = logging.getLogger(__name__)


class DoublePlikeObserver(AbstractNodeObserver):
    """
    Observer for <p/> and <ab/> elements with parent <p/> or <ab/>.

    Find <p/> and <ab/> elements that have <p/> or <ab/> as parent
    and strip the inner tag (text and tail as well as the children
    of the inner element will be preserved).
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
        if self.action == "add-lb":
            self._add_linebreak_to_separate_text_parts(node)
        merge_into_parent(node)

    def configure(self, config_dict: Dict[str, str]) -> None:
        action = config_dict.get("action", None)
        if action is not None:
            self.action = action
        else:
            logger.warning("Invalid configuration, using default.")

    def _add_linebreak_to_separate_text_parts(self, node: etree._Element) -> None:
        parent = node.getparent()
        if (parent.text is not None and parent.text.strip()) and (
            node.text is not None
            and node.text.strip()
            or (node.tail is not None and node.tail.strip() and len(node) == 0)
        ):
            pass
            new_lb = create_new_element(node, "lb")
            insert_index = parent.index(node)
            parent.insert(insert_index, new_lb)
