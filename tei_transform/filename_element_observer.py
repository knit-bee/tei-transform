from lxml import etree


class FilenameElementObserver:
    xpattern = "//filename"

    def observe(self, node: etree._Element) -> bool:
        if node.xpath(self.xpattern):
            return True
        return False
