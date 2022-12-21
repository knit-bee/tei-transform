import os
import subprocess
import tempfile


def test_package_callable_without_error():
    process = subprocess.run(
        ["tei-transform", "--help"], check=True, capture_output=True
    )
    assert process.returncode == 0


def test_package_callable_with_arguments():
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_file = tempfile.mkstemp(".xml", dir=tempdir, text=True)
        with open(tmp_file, "w") as fp:
            fp.write("<element/>")
        process = subprocess.run(
            ["tei-transform", tmp_file, "-t", "teiheader-type", "-o", tempdir],
            capture_output=True,
        )
    assert process.returncode == 0


def test_run_with_config_file():
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_file = tempfile.mkstemp(".xml", dir=tempdir, text=True)
        with open(tmp_file, "w") as fp:
            fp.write("<element/>")
        _, tmp_conf = tempfile.mkstemp(dir=tempdir, text=True)
        with open(tmp_conf, "w") as ptr:
            ptr.write("[revision]")
        process = subprocess.run(
            [
                "tei-transform",
                tmp_file,
                "-t",
                "teiheader-type",
                "-c",
                tmp_conf,
                "-o",
                tempdir,
            ],
            capture_output=True,
        )
    assert process.returncode == 0


def test_validaton_scheme_file_found():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tempdir:
        _, tmp_file = tempfile.mkstemp(".xml", dir=tempdir, text=True)
        with open(tmp_file, "w") as fp:
            fp.write("<element/>")
        os.chdir(tempdir)
        process = subprocess.run(
            ["tei-transform", tmp_file, "-t", "teiheader-type", "--copy-valid"],
            capture_output=True,
        )
    os.chdir(cwd)
    assert process.returncode == 0
