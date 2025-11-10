def extract_peptides(input_file, output_file):
    peptides = []    # Create an empty list to store the peptides we find

    # Open the input file to read its content
    with open(input_file, 'r') as f:             # Go through each line in the file
        for line in f:
            line = line.strip()    # Remove spaces at the start/end of the line

            # Skip lines that are empty, start with "#" or start with "Pos" (headers)
            if not line or line.startswith("#") or line.startswith("Pos"):
                continue  # Skip empty lines or headers directly go to the next line

            parts = line.split()    # Split the line into parts separated by spaces
            if "PEPLIST" in parts:     # Check if the line contains the word "PEPLIST"
                pep_index = parts.index("PEPLIST") - 1     # Find the peptide just before the word "PEPLIST"
                peptide = parts[pep_index]        # This is the peptide sequence
                peptides.append(peptide)    # Add it to the list
              
    with open(output_file, 'w') as f:     # write all extracted peptides to the output file
        for pep in peptides:
            f.write(f"{pep}\n")    # write each peptid eon a new line

    print(f"✅ Extracted {len(peptides)} peptides to: {output_file}")

# Example usage:
extract_peptides("strong_binders.txt", "kleb_peptides.txt")
extract_peptides("anx_strong_peptides.txt", "anx_peptides.txt")




