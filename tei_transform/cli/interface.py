import sys

from tei_transform.cli.controller import TeiTransformController
from tei_transform.cli.use_case import TeiTransformationUseCaseImpl


def main() -> None:
    args = sys.argv[1:]
    controller = TeiTransformController(TeiTransformationUseCaseImpl())
    controller.process_arguments(args)
