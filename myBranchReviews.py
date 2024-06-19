import json
import os

def append_excl_branch(file_path, line_number):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the line number is valid
    if line_number - 1 < len(lines):
        line_content = lines[line_number - 1].rstrip()
        excl_branch_comment = ' /* GCOVR_EXCL_BR_LINE */'
        excl_start = '/* GCOVR_EXCL_BR_START */\n'
        excl_stop = '/* GCOVR_EXCL_BR_STOP */\n'

        if __get_line_length(line_content) + len(excl_branch_comment) > 92:
            # Insert EXCL_START before the uncovered line
            lines.insert(line_number - 1, excl_start)
            # Insert EXCL_STOP after the uncovered line
            lines.insert(line_number + 1, excl_stop)

            print(lines[line_number-1])
            print(lines[line_number])
            print(lines[line_number+1])
        else:
            # Append the comment to the specified line
            lines[line_number - 1] = line_content + excl_branch_comment + '\n'

        # Write the updated lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Updated branch line {line_number} in {file_path}")
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
        
        # Process branch coverage
        for line in lines_to_process:
            for branch in line.get("branches", []):
                if branch["count"] == 0:
                    append_excl_branch(file_path, line["line_number"])
                    break

def __get_line_length(line_content: str) -> int:
    return sum(4 if char == '\t' else 1 for char in line_content)

if __name__ == "__main__":
    coverage_file_path = 'twister-out/coverage.json'
    process_coverage_file(coverage_file_path)
