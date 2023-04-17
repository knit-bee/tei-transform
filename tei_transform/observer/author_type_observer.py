import logging
from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import remove_attribute_from_node

logger = logging.getLogger(__name__)


class AuthorTypeObserver(AbstractNodeObserver):
    """
    Handle attribute @type of <author/> elements.

    Default transformation consists of deletion of
    the @type attribute.
    Configure by setting the action to 'replace' to
    the replace @type by @role.
    """

    def __init__(self, action: Optional[str] = None) -> None:
        self.action = action

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node.tag).localname == "author" and "type" in node.attrib:
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if self.action == "replace":
            attr_value = node.attrib.pop("type")
            node.set("role", attr_value)
        else:
            remove_attribute_from_node(node, "type")

    def configure(self, config_dict: Dict[str, str]) -> None:
        action = config_dict.get("action", None)
        if action is not None:
            self.action = action
        else:
            logger.warning("Invalid configuration, using default.")
