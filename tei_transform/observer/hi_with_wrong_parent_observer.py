import logging

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element

logger = logging.getLogger(__name__)


class HiWithWrongParentObserver(AbstractNodeObserver):
    """
    Observer for <hi/> elements that are children of <body/> or <div/>

    Find <hi/> elements that are children of either <body/> or a div on
    any level. If the parent element is <body/>, the <hi/> element will be
    wrapped in a <p/> element. If the parent is <div#/>, the <hi/> element
    is embedded in a <div#/> with the according number and a <p/>.
    """

    def observe(self, node: etree._Element) -> bool:
        if etree.QName(node).localname == "hi":
            if etree.QName(node.getparent()).localname in {
                "body",
                "div",
                "div1",
                "div2",
                "div3",
                "div4",
                "div5",
                "div6",
                "div7",
            }:
                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        ns_prefix = node.nsmap.get(None, None)
        # check if text or tail of <hi/> is not empty
        if (node.text is not None and node.text.strip()) or (
            node.tail is not None and node.tail.strip()
        ):
            div_tags = [etree.QName(ns_prefix, f"div{i}").text for i in range(1, 8)] + [
                etree.QName(ns_prefix, "div").text
            ]
            div_siblings = list(parent.iterchildren(div_tags))
            node_index = parent.index(node)
            if div_siblings != []:
                possible_div_tags = {node.tag for node in div_siblings}.intersection(
                    div_tags
                )
                if len(possible_div_tags) != 1:
                    logger.warning(
                        "<div#/> elements with conflicting levels found on the same level "
                        f"at {node.sourceline}. Transformation for <hi/> not applied. "
                    )
                    return
                sibling_div_tag = possible_div_tags.pop()
                new_div_tag = etree.QName(sibling_div_tag).localname
                new_div = create_new_element(node, new_div_tag)
                new_p = create_new_element(node, "p")
                parent.insert(node_index, new_div)
                new_div.append(new_p)
                new_p.append(node)
            else:
                new_p = create_new_element(node, "p")
                parent.insert(node_index, new_p)
                new_p.append(node)

        else:
            parent.remove(node)
