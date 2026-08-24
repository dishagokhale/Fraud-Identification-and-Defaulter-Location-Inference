# ✅ This script removes leading and trailing quotes from each line of the CSV

input_file = "selected_features_clean.csv"   # your current file
output_file = "fixed.csv"                    # cleaned file

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        # If a line starts and ends with a quote, strip them
        if line.startswith('"') and line.endswith('"\n'):
            outfile.write(line[1:-2] + '\n')  # Remove the first and last quote
        elif line.startswith('"') and line.endswith('"'):  
            outfile.write(line[1:-1] + '\n')  # Handles last line without newline
        else:
            outfile.write(line)

print("✅ Fixed CSV created successfully as fixed.csv")
