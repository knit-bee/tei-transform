from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.element_transformation import create_new_element


class BylineSiblingObserver(AbstractNodeObserver):
    """
    Observer for siblings after <byline/> elements that violate
    TEI model.divWrapper.

    Find siblings of <byline/> elements where the <byline/> elements has
    siblings on both sides that are not part of model.divWrapper (i.e.
    have other tags than: 'argument', 'byline', 'dateline', 'docAuthor',
    'docDate', 'epigraph', 'signed', 'meeting', and 'salute' or 'head' and
    'opener' iff the sibling appears at the begining of a textual division).
    Add a new <div/> element wrapping all siblings before the violating
    sibling of <byline/> (up to <div/> if present). The following siblings
    are not touched, i.e. a <p/> might now appear as a sibling of <div/>.
    To avoid this invalid structure, use togehter with PAsDivSiblingObserver.
    """

    #  cf. https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.divWrapper.html
    div_wrapper = [
        "argument",
        "byline",
        "dateline",
        "docAuthor",
        "docDate",
        "epigraph",
        "signed",
        "meeting",
        "salute",
        "figure",
    ]
    head_like = [
        "head",
        "opener",
    ]

    def observe(self, node: etree._Element) -> bool:
        byline_siblings = list(node.itersiblings("{*}byline", preceding=True))
        if byline_siblings != []:
            if etree.QName(node).localname not in self.div_wrapper + self.head_like:
                for byline_element in byline_siblings:
                    siblings_before_invalid_tags = [
                        etree.QName(sibling).localname
                        not in self.head_like + self.div_wrapper
                        for sibling in byline_element.itersiblings(preceding=True)
                    ]
                    if siblings_before_invalid_tags:
                        siblings_after_invalid_tags = [
                            etree.QName(sibling).localname not in self.div_wrapper
                            for sibling in byline_element.itersiblings(preceding=False)
                        ]
                        if siblings_after_invalid_tags:
                            if any(siblings_after_invalid_tags) and any(
                                siblings_before_invalid_tags
                            ):
                                return True
        return False

    def transform_node(self, node: etree._Element) -> None:
        parent = node.getparent()
        older_siblings = []
        for sibling in node.itersiblings(preceding=True):
            if etree.QName(sibling).localname == "div":
                break
            older_siblings.append(sibling)
        new_div = create_new_element(node, "div")
        node_index = parent.index(node)
        parent.insert(node_index, new_div)
        for sibling in reversed(older_siblings):
            new_div.append(sibling)
