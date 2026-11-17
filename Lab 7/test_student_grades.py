from hypothesis import given, strategies as st
from student_grades import average_marks, parse_srn, short_name

@given(st.text() | st.none())
def test_average_marks_no_crash(s):

@given(st.text() | st.none())
def test_parse_srn_no_crash(s):

@given(st.text() | st.none())
def test_short_name_no_crash(s):
