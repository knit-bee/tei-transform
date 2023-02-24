import configparser
import datetime
import logging
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RevisionDescChange:
    person: List[str]
    date: str
    reason: str


logger = logging.getLogger(__name__)


def parse_config_file(file: str) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(file)
    return config


def construct_change_from_config(
    config: configparser.ConfigParser,
) -> Optional[RevisionDescChange]:
    """
    Extract data from [revision] section in config, where the information
    for the change is stored.
    Return a RevisionDescChange with the gathered information.
    In the config file, the [revision] section should specify a 'person'
    responsible for the change and a 'reason' how the file was changed. An
    optional 'date' can also be indicated. If 'date' is missing, the current
    date will be used.
    """
    if "revision" not in config.sections():
        logger.warning("No section [revision] found in config file.")
        return None
    revision = config["revision"]
    person_entry = revision.get("person", "")
    person = [
        clean_name for name in person_entry.split(",") if (clean_name := name.strip())
    ]
    reason = revision.get("reason", None)
    date_entry = revision.get("date", "")
    try:
        date = datetime.date.fromisoformat(date_entry)
    except ValueError:
        logger.info("No valid date specified, using today's date.")
        date = datetime.date.today()
    return RevisionDescChange(person=person, date=date.isoformat(), reason=reason)
