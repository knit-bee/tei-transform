import subprocess


def test_package_callable_without_error():
    process = subprocess.run(
        ["tei-transform", "--help"], check=True, capture_output=True
    )
    assert process.returncode == 0


def test_package_callable_with_arguments():
    process = subprocess.run(
        ["tei-transform", "file.xml", "-t", "teiheader"], capture_output=True
    )
    assert process.returncode == 0
