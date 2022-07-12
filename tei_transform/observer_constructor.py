from lxml import etree


def check_if_observer_pattern_is_valid_xpath(pattern: str) -> bool:
    dummy_tree = etree.XML("<tree/>")
    try:
        dummy_tree.xpath(pattern)
        return True
    except etree.XPathEvalError:
        return False


class ObserverConstructor:
    def __init__(self) -> None:
        pass
