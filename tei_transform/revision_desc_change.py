import configparser
import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RevisionDescChange:
    person: List[str]
    date: str
    reason: str


def construct_change_from_config_file(file: str) -> Optional[RevisionDescChange]:
    config = configparser.ConfigParser()
    config.read(file)
    if "revision" not in config.sections():
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
        date = None
    if date is None:
        date = datetime.date.today()
    return RevisionDescChange(person=person, date=date.isoformat(), reason=reason)
