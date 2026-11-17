def average_marks(marks_csv):
    if not isinstance(marks_csv, str):
        raise TypeError("marks must be provided as a CSV string")

    marks = []
    for mark_text in marks_csv.split(','):
        mark_text = mark_text.strip()
        if not mark_text or len(mark_text) > 3:
            raise ValueError("marks must be integers from 0 to 100")
        mark = int(mark_text)
        if mark < 0 or mark > 100:
            raise ValueError("marks must be integers from 0 to 100")
        marks.append(mark)

    if not marks:
        raise ValueError("at least one mark is required")
    return round(sum(marks) / len(marks), 2)

def parse_srn(srn):
    if not isinstance(srn, str):
        raise TypeError("SRN must be a string")
    if (
        len(srn) != 13
        or srn[:6] != "PES1UG"
        or not srn[6:8].isdigit()
        or not srn[8:10].isalpha()
        or not srn[10:].isdigit()
    ):
        raise ValueError("invalid SRN format")
    return srn[:4], int(srn[6:8]), srn[8:10]

def short_name(full_name):
    if not isinstance(full_name, str):
        raise TypeError("full name must be a string")
    parts = full_name.split()
    if len(parts) != 2:
        raise ValueError("full name must contain exactly two words")
    first, last = parts
    return first[0].upper() + ". " + last.capitalize()

def main():
    print("==== Running average_marks ====")
    user_input = input("Enter marks as CSV (e.g. 78,85,92): ")
    result = average_marks(user_input)
    print("Average Marks:", result)

    print("\n==== Running parse_srn ====")
    user_input = input("Enter an SRN (e.g. PES1UG23CS123): ")
    result = parse_srn(user_input)
    print("Campus, Year and Dept:", result)

    print("\n==== Running short_name ====")
    user_input = input("Enter first and last name (e.g. ravi kumar): ")
    result = short_name(user_input)
    print("Short Name:", result)

if __name__ == "__main__":
    main()
