from Bio import SeqIO

def generate_filtered_peptides(fasta_file, min_peptide_length=9, max_peptide_length=12):
    """
    Generate and save filtered peptides from a FASTA file.
    Peptides must follow these rules:
    - 1st residue: small (A, G, S, T)
    - 2nd residue: positively charged (R, K)
    - Last residue: hydrophobic/aromatic (L, F, Y, M, V, W, I)
    """

    # Amino acid preferences
    first_residues = ["A", "G", "S", "T"]
    second_residues = ["R", "K"]
    last_residues = ["L", "F", "Y", "M", "V", "W", "I"]

    filtered_peptides = []

    # Read the FASTA file
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(record.seq)
        print(f"Processing {fasta_file}: sequence length = {len(sequence)}")

        # Generate peptides for lengths between min and max
        for peptide_length in range(min_peptide_length, max_peptide_length + 1):
            for i in range(len(sequence) - peptide_length + 1):
                peptide = sequence[i:i + peptide_length]

                # Apply filtering rules
                if (
                    peptide[0] in first_residues and
                    peptide[1] in second_residues and
                    peptide[-1] in last_residues
                ):
                    filtered_peptides.append(peptide)

    print(f"✅ Total filtered peptides: {len(filtered_peptides)}")

    # --- Save results to both files ---
    for ext in [".fasta", ".txt"]:
        output_name = f"output{ext}"
        with open(output_name, "w") as file:
            for peptide in filtered_peptides:
                file.write(peptide + "\n")
        print(f"💾 Saved peptides to {output_name}")


# Example usage
if __name__ == "__main__":
    fasta_file = "filename.fasta"    # type your fasta file name in place of filename.fasta
    generate_filtered_peptides(fasta_file)
