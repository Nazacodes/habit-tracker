from habit_tracker.validation import MAX_DESCRIPTION_LEN, MAX_NAME_LEN, validate_habit_fields


def test_validate_requires_name():
    ok, msg = validate_habit_fields("", "")
    assert not ok


def test_validate_name_length_boundary():
    name = "a" * MAX_NAME_LEN
    assert validate_habit_fields(name, "")[0] is True
    assert validate_habit_fields(name + "!", "")[0] is False


def test_validate_description_length_boundary():
    desc = "d" * MAX_DESCRIPTION_LEN
    assert validate_habit_fields("Ok", desc)[0] is True
    assert validate_habit_fields("Ok", desc + "!")[0] is False

