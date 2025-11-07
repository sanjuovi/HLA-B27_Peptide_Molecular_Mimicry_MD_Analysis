# Function to separate SB and WB binders with tags
def separate_binders_with_tags(input_file, strong_file="strong_binders.txt", weak_file="weak_binders.txt"):
    strong_lines = []
    weak_lines = []
    label = "[" + input_file.split("_netmpchen")[0] + "]"  # e.g., [peptides_chunk1]

    with open(input_file, 'r') as f:
        for line in f:
            if "SB" in line:
                strong_lines.append(f"{label} {line}")
            elif "WB" in line:
                weak_lines.append(f"{label} {line}")

    with open(strong_file, 'a') as sf:
        sf.writelines(strong_lines)

    with open(weak_file, 'a') as wf:
        wf.writelines(weak_lines)


# Main script to process all 9 files
if __name__ == "__main__":
    # List of your NetMHCpan result files
    input_files = [
        "peptides_chunk1_netmpchen.txt",
        "peptides_chunk2_netmpchen.txt",
        "peptides_chunk3_netmpchen.txt",
        "peptides_chunk4_netmpchen.txt",
        "peptides_chunk5_netmpchen.txt",
        "peptides_chunk6_netmpchen.txt",
        "peptides_chunk7_netmpchen.txt",
        "peptides_chunk8_netmpchen.txt",
        "peptides_chunk9_netmpchen.txt"
    ]

    # Optional: Clear output files before appending
    open("strong_binders.txt", "w").close()
    open("weak_binders.txt", "w").close()

    # Process each file
    for file in input_files:
        separate_binders_with_tags(file)




