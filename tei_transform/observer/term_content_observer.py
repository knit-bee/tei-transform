import logging
from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver

logger = logging.getLogger(__name__)


class TermContentObserver(AbstractNodeObserver):
    """
    Observer for <term/> elements with <keywords/> as parent.

    Find <term/> elements with <keywords/> parent and check if the
    first <term/> element contains the desired text content. If not,
    a new <term/> element is added.
    If the first element empty or only contains ',', it is overwritten.
    This requires configuration to set the desired content of the
    <term/> element.
    """

    def __init__(self, term_content: Optional[str] = None) -> None:
        self.config_required: bool = True
        self.term_content = term_content

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "term":
            parent = node.getparent()
            if etree.QName(parent).localname == "keywords":
                if parent.index(node) == 0 and (
                    node.text is None or node.text != self.term_content
                ):
                    return True
                if node.text is not None and node.text.strip() == ",":
                    return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        pass

    def configure(self, config_dict: Dict[str, str]) -> None:
        term_content = config_dict.get("content")
        if not term_content:
            logger.warning("Invalid configuration for TermContentObserver")
            return
        self.term_content = term_content
