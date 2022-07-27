import configparser
import datetime
from dataclasses import dataclass
from typing import List, Optional
import logging


@dataclass
class RevisionDescChange:
    person: List[str]
    date: str
    reason: str


logger = logging.getLogger(__name__)


def construct_change_from_config_file(file: str) -> Optional[RevisionDescChange]:
    """
    Read config file and extract data from [revision] section,
    where the information for the change is stored.
    Return a RevisionDescChange with the gathered information.
    In the config file, the [revision] section should specify a 'person'
    responsible for the change and a 'reason' why the file was changed. An
    optional 'date' can also be named. If 'date' is missing, the current
    date will be used.
    """
    config = configparser.ConfigParser()
    config.read(file)
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
        date = None
    if date is None:
        date = datetime.date.today()
    return RevisionDescChange(person=person, date=date.isoformat(), reason=reason)
