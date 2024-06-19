import json

def append_excl_br_line(file_path, line_number):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the line number is valid
    if line_number - 1 < len(lines):
        # Append the comment to the specified line
        lines[line_number - 1] = lines[line_number - 1].rstrip() + ' /* GCOVR_EXCL_BR_LINE */\n'

        # Write the updated lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Updated line {line_number} in {file_path}")
    else:
        print(f"Warning: Line number {line_number} is out of range for file {file_path}")

def process_coverage_file_for_branches(coverage_file):
    with open(coverage_file, 'r') as f:
        coverage_data = json.load(f)

    for file in coverage_data["files"]:
        file_path = file["file"]
        for line in file["lines"]:
            for branch in line.get("branches", []):
                if branch["count"] == 0:
                    append_excl_br_line(file_path, line["line_number"])
                    break  # Only append once per line even if multiple branches are uncovered

if __name__ == "__main__":
    coverage_file_path = 'twister-out/coverage.json'  # Replace with your actual coverage JSON file path
    process_coverage_file_for_branches(coverage_file_path)

