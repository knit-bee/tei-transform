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
            ["tei-transform", tmp_file, "-t", "teiheader"], capture_output=True
        )
    assert process.returncode == 0
