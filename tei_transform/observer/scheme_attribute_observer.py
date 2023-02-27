from typing import Dict, Optional

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class SchemeAttributeObserver(AbstractNodeObserver):
    """
    Observer for <classCode/> elements with @scheme attribute with empty value.

    Find <classCode/> elements with @scheme attribute that has only an empty
    string as value and set new value.
    """

    def __init__(self, scheme: Optional[str] = None) -> None:
        self.scheme = scheme

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
