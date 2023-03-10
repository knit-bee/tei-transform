import logging
from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver

logger = logging.getLogger(__name__)


class SchemeAttributeObserver(AbstractNodeObserver):
    """
    Observer for <classCode/> elements with @scheme attribute with empty value.

    Find <classCode/> elements with @scheme attribute that has only an empty
    string as value and set new value. This requires configuration by
    setting the scheme path that should be used as value or configuration
    to remove the <classCode/> element from the tree.
    """

    def __init__(self, scheme: Optional[str] = None) -> None:
        self.scheme = scheme
        self.config_required: bool = True
        self.action: Optional[str] = None

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname.lower() == "classcode"
            and node.attrib.get("scheme", None) == ""
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        if self.scheme is not None:
            node.set("scheme", self.scheme)
        elif self.action == "remove":
            parent = node.getparent()
            parent.remove(node)
        else:
            logger.warning("Invalid configuration for SchemeAttributeObserver")

    def configure(self, config_dict: Dict[str, str]) -> None:
        scheme_path = config_dict.get("scheme", None)
        action = config_dict.get("action", None)
        if scheme_path is not None:
            self.scheme = scheme_path
        if action is not None:
            self.action = action
        else:
            logger.warning("Invalid configuration for SchemeAttributeObserver.")
