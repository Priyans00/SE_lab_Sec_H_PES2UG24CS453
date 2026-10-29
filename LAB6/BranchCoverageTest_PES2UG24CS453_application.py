import pytest

from student_grades import exam_eligibility, final_marks, letter_grade


@pytest.mark.parametrize(
    ("marks", "expected"),
    [
        (0, "F"),
        (40, "E"),
        (50, "D"),
        (60, "C"),
        (70, "B"),
        (80, "A"),
        (90, "S"),
        (100, "S"),
    ],
)
def test_letter_grade_each_grade_branch(marks, expected):
    assert letter_grade(marks) == expected


@pytest.mark.parametrize("marks", [-1, 101])
def test_letter_grade_validation_branches(marks):
    with pytest.raises(ValueError, match="invalid marks"):
        letter_grade(marks)


def test_final_marks_validation_short_circuits_after_invalid_internal():
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(41, 60, False)


def test_final_marks_validation_evaluates_external_invalid_branch():
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(40, 61, False)


def test_final_marks_without_project_branch():
    assert final_marks(20, 30, False) == 50


def test_final_marks_project_bonus_without_cap_branch():
    assert final_marks(20, 30, True) == 55


def test_final_marks_project_bonus_cap_branch():
    assert final_marks(40, 60, True) == 100


def test_exam_eligibility_blocked_branch():
    assert exam_eligibility(100, False, False) == "blocked"


def test_exam_eligibility_attendance_branch():
    assert exam_eligibility(75, True, False) == "eligible"


def test_exam_eligibility_medical_condition_true_branch():
    assert exam_eligibility(65, True, True) == "eligible"


def test_exam_eligibility_medical_condition_false_branch():
    assert exam_eligibility(65, True, False) == "detained"


def test_exam_eligibility_attendance_below_medical_threshold_branch():
    assert exam_eligibility(64, True, True) == "detained"
