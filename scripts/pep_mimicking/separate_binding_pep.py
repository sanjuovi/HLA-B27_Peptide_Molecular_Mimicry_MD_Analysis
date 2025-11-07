def separate_binding_peptides(input_file, strong_file='strong_binders.txt', weak_file='weak_binders.txt'):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    strong_lines = []
    weak_lines = []

    for line in lines:
        # Skip headers or empty lines
        if line.strip() == "" or line.startswith("#") or line.lower().startswith("pos") or line.lower().startswith("allele"):
            continue

        # Check if SB or WB appears in the line
        if 'SB' in line:
            strong_lines.append(line)
        elif 'WB' in line:
            weak_lines.append(line)

    # Write to output files
    with open(strong_file, 'w') as sf:
        sf.writelines(strong_lines)

    with open(weak_file, 'w') as wf:
        wf.writelines(weak_lines)

    print(f"✅ Strong Binders saved to: {strong_file}")
    print(f"✅ Weak Binders saved to: {weak_file}")
    print(f"📊 Total Strong: {len(strong_lines)}, Weak: {len(weak_lines)}")

# Example usage:
separate_binding_peptides("peptides_chunk1_netmpchen.txt")



