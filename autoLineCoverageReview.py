import json
import os

def append_excl_line(file_path, line_number):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the line number is valid
    if line_number - 1 < len(lines):
        line_content = lines[line_number - 1].rstrip()
        excl_line_comment = ' /* GCOVR_EXCL_LINE */'
        excl_start = '/* GCOVR_EXCL_START */\n'
        excl_stop = '/* GCOVR_EXCL_STOP */\n'

        if __get_line_length(line_content) + len(excl_line_comment) > 92:
            # Insert EXCL_START and EXCL_STOP comments around the line
            #lines[line_number - 1] = f'/* GCOVR_EXCL_START */\n{line_content}\n/* GCOVR_EXCL_STOP */\n'

            __insert_excl_comments(lines, line_number, excl_start, excl_stop)
        else:
            # Append the comment to the specified line
            lines[line_number - 1] = line_content + excl_line_comment + '\n'

        # Write the updated lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Updated line {line_number} in {file_path}")
    else:
        print(f"Warning: Line number {line_number} is out of range for file {file_path}")

def process_coverage_file(coverage_file):
    with open(coverage_file, 'r') as f:
        coverage_data = json.load(f)

    # Process files in reverse order
    for file in coverage_data["files"]:
        file_path = file["file"]
        # Collect lines in reverse order to avoid messing up line numbers
        lines_to_process = sorted(file["lines"], key=lambda x: x["line_number"], reverse=True)
        for line in lines_to_process:
            if line["count"] == 0 and not line.get("gcovr/excluded", False):
                append_excl_line(file_path, line["line_number"])


def __get_line_length(line_content: str) -> int:
    return sum(4 if char == '\t' else 1 for char in line_content)

def __insert_excl_comments(lines, line_number, excl_start, excl_stop):
    # Insert EXCL_START comment
    lines.insert(line_number - 1, excl_start)
    # Find the next line with a semicolon
    semicolon_line_number = line_number
    while semicolon_line_number - 1 < len(lines) and ';' not in lines[semicolon_line_number - 1]:
        semicolon_line_number += 1
    # Add EXCL_STOP comment after the line with the semicolon
    if semicolon_line_number - 1 < len(lines):
        lines.insert(semicolon_line_number, excl_stop)
    else:
        lines.append(excl_stop)

if __name__ == "__main__":
    coverage_file_path = 'twister-out/coverage.json'
    process_coverage_file(coverage_file_path)

