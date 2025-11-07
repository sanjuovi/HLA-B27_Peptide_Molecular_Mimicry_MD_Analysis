from Bio import SeqIO

def generate_filtered_peptides(fasta_file, min_peptide_length=9, max_peptide_length=12):
    # Define residue preferences
    first_residues = ["A", "G", "S", "T"]
    second_residues = ["R", "K"]
    last_residues = ["L", "F", "Y", "M", "V", "W", "I"]

    output_file = f"generated_kleb_peps_with_rule.txt"
    total_filtered_peptides = []

    print(f"📂 Processing: {fasta_file}")
    
    # Parse all sequences in the FASTA
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(record.seq)
        
        for pep_len in range(min_peptide_length, max_peptide_length + 1):
            for i in range(len(sequence) - pep_len + 1):
                peptide = sequence[i:i + pep_len]
                
                # Apply the rule: Small - Positively Charged - Hydrophobic
                if (peptide[0] in first_residues and
                    peptide[1] in second_residues and
                    peptide[-1] in last_residues):
                    total_filtered_peptides.append(peptide)

    # Save results to file
    with open(output_file, "w") as f:
        for pep in total_filtered_peptides:
            f.write(pep + "\n")

    print(f"✅ Done! {len(total_filtered_peptides)} peptides saved to: {output_file}")


# Call the function
if __name__ == "__main__":
    generate_filtered_peptides(
        fasta_file="uniprotkb_proteome_UP000000265_K_pneumoniae_strain_ATCC700721_MGH_78578.fasta",
        min_peptide_length=9,
        max_peptide_length=12
    )




