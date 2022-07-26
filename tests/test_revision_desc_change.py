import tempfile
import os
import datetime
from tei_transform.revision_desc_change import (
    construct_change_from_config_file,
    RevisionDescChange,
)


def test_data_parsed_correctly_from_config_file():
    change = construct_change_from_config_file(
        os.path.join("tests", "testdata", "revision.config")
    )
    expected_change = RevisionDescChange(
        person=["Some Name"],
        date="2022-05-23",
        reason="The reason why the file was changed",
    )
    assert change == expected_change


def test_current_date_inserted_when_not_defined():
    conf_string = """
    [revision]
    person = Person Name
    reason = Some reason"""
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_conf = tempfile.mkstemp(".ini", dir=tempdir, text=True)
        with open(tmp_conf, "w") as ptr:
            ptr.write(conf_string)
        change = construct_change_from_config_file(tmp_conf)
    assert change.date == datetime.date.today().isoformat()


def test_multiple_person_names_parsed_correctly():
    conf_string = """
    [revision]
    person = First Name, Second Name
    reason = Some reason"""
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_conf = tempfile.mkstemp(".ini", dir=tempdir, text=True)
        with open(tmp_conf, "w") as ptr:
            ptr.write(conf_string)
        change = construct_change_from_config_file(tmp_conf)
    assert change.person == ["First Name", "Second Name"]


def test_malformed_config_file_returns_none():
    conf_string = """
[revisionDesc]
person = Person Name
reason = Some reason"""
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_conf = tempfile.mkstemp(".ini", dir=tempdir, text=True)
        with open(tmp_conf, "w") as ptr:
            ptr.write(conf_string)
        change = construct_change_from_config_file(tmp_conf)
    assert change is None


def test_none_inserted_for_missing_reason():
    conf_string = """
[revision]
"""
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_conf = tempfile.mkstemp(".ini", dir=tempdir, text=True)
        with open(tmp_conf, "w") as ptr:
            ptr.write(conf_string)
        change = construct_change_from_config_file(tmp_conf)
    assert change.reason is None


def test_empty_list_returned_for_missing_person():
    conf_string = """
    [revision]
"""
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_conf = tempfile.mkstemp(".ini", dir=tempdir, text=True)
        with open(tmp_conf, "w") as ptr:
            ptr.write(conf_string)
        change = construct_change_from_config_file(tmp_conf)
    assert change.person == []
