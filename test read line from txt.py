with open("user_data_file.txt", "r") as file:
    first_line = file.readline().strip()
    second_line = file.readline().strip()


def check_content(line_number, line):
    print(f"{line} is in line {line_number}")


check_content(1, first_line)
check_content(2, second_line)