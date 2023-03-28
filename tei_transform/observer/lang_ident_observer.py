import logging
from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver

logger = logging.getLogger(__name__)


class LangIdentObserver(AbstractNodeObserver):
    """
    Observer for <language/> that are missing @ident attribute.

    Find <language/> elements with missing @ident attribute and
    set new value. The value to be set as attribute can be passed
    via configuration.
    If there are multiple <language/> elements present in the source
    file, the language codes are matched via index.
    """

    def __init__(self, ident: Optional[Dict[int, str]] = None) -> None:
        self.ident = ident or {}

    def observe(self, node: etree._Element) -> bool:
        if (
            etree.QName(node).localname == "language"
            and node.attrib.get("ident", None) is None
        ):
            return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        for i, lang_child in enumerate(parent.findall("{*}language")):
            if lang_child is node:
                node.set("ident", self.ident.get(i, ""))
                break

    def configure(self, config_dict: Dict[str, str]) -> None:
        ident_attr = config_dict.get("ident", None)
        if ident_attr is not None:
            self.ident = {
                i: lang.strip() for i, lang in enumerate(ident_attr.split(","))
            }
        else:
            logger.warning(
                "Invalid configuration for LangIdentObserver, setting empty string for @ident."
            )
