from lxml import etree


class IdAttributeObserver:
    xpattern = "//*[@id]"

    def observe(self, node: etree._Element) -> bool:
        if node.xpath(self.xpattern):
            return True
        return False
