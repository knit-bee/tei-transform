import logging
import os.path
import sys

from tei_transform.cli.controller import TeiTransformController
from tei_transform.cli.use_case import TeiTransformationUseCaseImpl
from tei_transform.observer_constructor import ObserverConstructor
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator
from tei_transform.xml_writer import XmlWriterImpl

logging.basicConfig(
    filename="tei-transform.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
)
logger = logging.getLogger()


def main() -> None:
    """
    Function that serves as entry point for console script.
    """
    args = sys.argv[1:]

    xml_iterator = XMLTreeIterator()
    tei_transformer = TeiTransformer(xml_iterator)
    xml_writer = XmlWriterImpl()
    observer_constructor = ObserverConstructor()
    tei_scheme = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "tei_all.rng"
    )

    use_case = TeiTransformationUseCaseImpl(
        xml_writer=xml_writer,
        tei_transformer=tei_transformer,
        observer_constructor=observer_constructor,
        tei_scheme=tei_scheme,
    )
    controller = TeiTransformController(use_case)
    controller.process_arguments(args)
