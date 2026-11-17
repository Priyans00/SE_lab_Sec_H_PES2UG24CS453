import pytest
from hypothesis import given, settings, strategies as st

from student_grades import average_marks, parse_srn, short_name


hypothesis_settings = settings(max_examples=100, deadline=None)


valid_marks_csv = st.lists(
    st.integers(min_value=0, max_value=100),
    min_size=1,
).map(lambda marks: ",".join(str(mark) for mark in marks))

invalid_marks_input = st.one_of(
    st.none(),
    st.just(""),
    st.just(","),
    st.just("10,,20"),
    st.just("10,abc,20"),
    st.just("10.5,20"),
    st.text(min_size=1000, max_size=2000),
    st.integers(),
    st.lists(st.integers()),
    st.dictionaries(st.text(min_size=1), st.integers()),
    st.lists(st.integers(min_value=-1000, max_value=-1), min_size=1).map(
        lambda marks: ",".join(str(mark) for mark in marks)
    ),
    st.integers(min_value=101).map(str),
)


@hypothesis_settings
@given(valid_marks_csv)
def test_average_marks_returns_the_rounded_mean(marks_csv):
    marks = [int(mark) for mark in marks_csv.split(",")]

    result = average_marks(marks_csv)

    assert isinstance(result, (int, float))
    assert result == round(sum(marks) / len(marks), 2)
    assert 0 <= result <= 100


@hypothesis_settings
@given(invalid_marks_input)
def test_average_marks_rejects_invalid_input(value):
    with pytest.raises((TypeError, ValueError)):
        average_marks(value)


valid_srn = st.builds(
    lambda year, department, number: f"PES1UG{year:02d}{department}{number:03d}",
    year=st.integers(min_value=0, max_value=99),
    department=st.text(
        alphabet=st.characters(
            whitelist_categories=("Lu",),
            blacklist_characters=" ",
        ),
        min_size=2,
        max_size=2,
    ),
    number=st.integers(min_value=0, max_value=999),
)

invalid_srn = st.one_of(
    st.none(),
    st.just(""),
    st.just("PES1UG23CS12"),
    st.just("PES1UGXXCS123"),
    st.just("BAD1UG23CS123"),
    st.just("PES1UG23CS12A"),
    st.text(min_size=1000, max_size=2000),
    st.text(min_size=1, max_size=200),
    st.integers(),
    st.lists(st.text()),
    st.dictionaries(st.text(min_size=1), st.integers()),
)


@hypothesis_settings
@given(valid_srn)
def test_parse_srn_returns_campus_year_and_department(srn):
    campus, year, department = parse_srn(srn)

    assert isinstance(campus, str)
    assert isinstance(year, int)
    assert isinstance(department, str)
    assert (campus, year, department) == ("PES1", int(srn[6:8]), srn[8:10])


@hypothesis_settings
@given(invalid_srn)
def test_parse_srn_rejects_invalid_input(value):
    with pytest.raises((TypeError, ValueError)):
        parse_srn(value)


name_word = st.text(
    alphabet=st.characters(
        whitelist_categories=("Ll", "Lu"),
        blacklist_characters=" ",
    ),
    min_size=1,
    max_size=40,
)

valid_full_name = st.tuples(name_word, name_word).map(
    lambda parts: f"{parts[0]} {parts[1]}"
)

invalid_full_name = st.one_of(
    st.none(),
    st.just(""),
    st.just("ravi"),
    st.just("ravi kumar shetty"),
    st.just("ravi\tkumar\nshetty"),
    st.text(min_size=1000, max_size=2000),
    st.integers(),
    st.lists(st.text()),
    st.dictionaries(st.text(min_size=1), st.text()),
)


@hypothesis_settings
@given(valid_full_name)
def test_short_name_returns_an_initial_and_capitalized_surname(full_name):
    first, last = full_name.split()

    result = short_name(full_name)

    assert isinstance(result, str)
    assert result == f"{first[0].upper()}. {last.capitalize()}"
    assert result.startswith(f"{first[0].upper()}. ")


@hypothesis_settings
@given(invalid_full_name)
def test_short_name_rejects_invalid_input(value):
    with pytest.raises((TypeError, ValueError)):
        short_name(value)
