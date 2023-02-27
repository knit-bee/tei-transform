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
    setting the scheme path that should be used as value.
    """

    def __init__(self, scheme: Optional[str] = None) -> None:
        self.scheme = scheme
        self.config_required = True

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

    def configure(self, config_dict: Dict[str, str]) -> None:
        scheme_path = config_dict.get("scheme", None)
        if scheme_path is not None:
            self.scheme = scheme_path
        else:
            logger.warning("Invalid configuration for SchemeAttributeObserver.")
