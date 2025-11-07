# Open the downloaded FASTA file and read the sequences
input_file = "uniprotkb_proteome_UP000000265_K_pneumoniae_strain_ATCC700721_MGH_78578.fasta"
output_file = "generated_kleb_peps_without_rule.txt"

# Function to slice peptides
def slice_peptides(sequence, min_len=9, max_len=12):
    peptides = []
    for i in range(len(sequence) - min_len + 1):
        for length in range(min_len, max_len + 1):
            peptide = sequence[i:i+length]
            peptides.append(peptide)
    return peptides

# Read the FASTA file and extract peptides
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    sequence = ""
    for line in infile:
        if line.startswith(">"):  # New protein sequence
            if sequence:  # Process the previous sequence
                peptides = slice_peptides(sequence)
                for peptide in peptides:
                    outfile.write(peptide + "\n")
            sequence = ""  # Reset sequence for new protein
        else:
            sequence += line.strip()  # Add sequence lines
    # Process the last sequence
    if sequence:
        peptides = slice_peptides(sequence)
        for peptide in peptides:
            outfile.write(peptide + "\n")

print("Peptide sequences have been sliced and saved to 'kp_peptides.txt'.")



