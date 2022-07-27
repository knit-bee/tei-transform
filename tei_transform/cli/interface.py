import logging
import sys

from tei_transform.cli.controller import TeiTransformController
from tei_transform.cli.use_case import TeiTransformationUseCaseImpl

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
    controller = TeiTransformController(TeiTransformationUseCaseImpl())
    controller.process_arguments(args)
