def extract_peptides(input_file, output_file):
    peptides = []

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#") or line.startswith("Pos"):
                continue  # Skip empty lines or headers

            parts = line.split()
            if "PEPLIST" in parts:
                pep_index = parts.index("PEPLIST") - 1
                peptide = parts[pep_index]
                peptides.append(peptide)

    with open(output_file, 'w') as f:
        for pep in peptides:
            f.write(f"{pep}\n")

    print(f"✅ Extracted {len(peptides)} peptides to: {output_file}")

# Example usage:
extract_peptides("strong_binders.txt", "kleb_peptides.txt")
extract_peptides("annexin_strong_peptides.txt", "annexin_peptides.txt")




