import pytest

from student_grades import exam_eligibility, final_marks, letter_grade


@pytest.mark.parametrize(
    ("marks", "expected"),
    [
        (100, "S"),
        (90, "S"),
        (89, "A"),
        (80, "A"),
        (79, "B"),
        (70, "B"),
        (69, "C"),
        (60, "C"),
        (59, "D"),
        (50, "D"),
        (49, "E"),
        (40, "E"),
        (39, "F"),
        (0, "F"),
    ],
)
def test_letter_grade_boundaries(marks, expected):
    assert letter_grade(marks) == expected


@pytest.mark.parametrize("marks", [-1, 101])
def test_letter_grade_rejects_marks_outside_range(marks):
    with pytest.raises(ValueError, match="invalid marks"):
        letter_grade(marks)


def test_final_marks_without_project():
    assert final_marks(32, 54, False) == 86


def test_final_marks_adds_project_bonus():
    assert final_marks(32, 54, True) == 91


def test_final_marks_caps_project_bonus_at_100():
    assert final_marks(40, 60, True) == 100


@pytest.mark.parametrize(
    ("internal", "external"),
    [
        (41, 0),
        (0, 61),
    ],
)
def test_final_marks_rejects_out_of_range_components(internal, external):
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(internal, external, False)


def test_exam_is_blocked_when_fees_are_unpaid():
    assert exam_eligibility(100, False, True) == "blocked"


def test_exam_is_eligible_with_required_attendance():
    assert exam_eligibility(75, True, False) == "eligible"


def test_exam_is_eligible_with_medical_exception():
    assert exam_eligibility(65, True, True) == "eligible"


def test_exam_is_detained_below_attendance_requirement():
    assert exam_eligibility(64, True, True) == "detained"


def test_exam_is_detained_without_medical_exception():
    assert exam_eligibility(65, True, False) == "detained"
