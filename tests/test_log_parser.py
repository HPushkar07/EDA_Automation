from main import parse_log


def test_extract_error():
    errors, warnings = parse_log("INFO: start\nERROR: invalid module")
    assert errors == ["ERROR: invalid module"]
    assert warnings == []


def test_extract_warning():
    errors, warnings = parse_log("Warning: unused signal\nDone")
    assert errors == []
    assert warnings == ["Warning: unused signal"]


def test_clean_log():
    assert parse_log("Compiled successfully\nPASS: and_gate") == ([], [])


def test_error_and_warning():
    errors, warnings = parse_log("FATAL: bad syntax\nWARNING: something unused")
    assert len(errors) == 1
    assert len(warnings) == 1
