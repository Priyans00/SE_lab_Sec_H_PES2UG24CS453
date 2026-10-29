import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

#Example test cases:
def test_s_grade():
    assert letter_grade(95) == "S"

def test_eligible():
    assert exam_eligibility(80, True, False) == "eligible"

#Write the rest of the test cases so that the code is 90- 100% covered.
