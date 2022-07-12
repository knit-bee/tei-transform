from lxml import etree


class IdAttributeObserver:
    xpattern = "//*[@id]"

    def observe(self, node: etree._Element) -> bool:
        if "id" in node.attrib:
            return True
        return False
