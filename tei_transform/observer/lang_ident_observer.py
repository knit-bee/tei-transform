import logging
from typing import Dict

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver

logger = logging.getLogger(__name__)


class LangIdentObserver(AbstractNodeObserver):
    """
    Observer for <language/> that are missing @ident attribute.
    """

    def __init__(self, ident: str = "") -> None:
        self.ident = ident

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "language"
            and node.attrib.get("ident", None) is None
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        node.set("ident", self.ident)

    def configure(self, config_dict: Dict[str, str]) -> None:
        ident_attr = config_dict.get("ident", None)
        if ident_attr is not None:
            self.ident = ident_attr
        else:
            logger.warning(
                "Invalid configuration for LangIdentObserver, setting empty string for @ident."
            )
