from Bio import SeqIO

# Input FASTA file name
fasta_file = "P07355_ANXA2_HUMAN_Annexin_A2.fasta"

# Output file
output_file = "all_anx_peps_without_rule.txt"

# Peptide lengths to slice
min_len = 9
max_len = 12

# Read protein sequence from FASTA
for record in SeqIO.parse(fasta_file, "fasta"):
    sequence = str(record.seq)

# Store sliced peptides
all_peptides = []

# Generate overlapping peptides from length 9 to 12
for length in range(min_len, max_len + 1):
    for i in range(len(sequence) - length + 1):
        peptide = sequence[i:i + length]
        all_peptides.append(peptide)

# Save peptides to file
with open(output_file, "w") as f:
    for pep in all_peptides:
        f.write(pep + "\n")

print(f"Saved {len(all_peptides)} peptides to {output_file}")



