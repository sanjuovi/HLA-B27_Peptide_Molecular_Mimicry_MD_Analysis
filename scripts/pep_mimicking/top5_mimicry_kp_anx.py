from Bio.Align import PairwiseAligner
from Bio.Seq import Seq

# Load peptide sequences from file
def load_peptides(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Function to align peptides and get matching scores
def align_peptides(kleb_peptides, annexin_peptide):
    aligner = PairwiseAligner()
    aligner.mode = 'global'  # Set alignment mode to global
    aligner.open_gap_score = -2  # Penalty for opening a gap
    aligner.extend_gap_score = -1  # Penalty for extending a gap

    mimic_data = []

    for kp in kleb_peptides:
        # Align the peptides using PairwiseAligner
        alignment = aligner.align(Seq(kp), Seq(annexin_peptide))
        best_alignment = alignment[0]  # Get the best alignment
        aln1, aln2 = str(best_alignment[0]), str(best_alignment[1])
        score = best_alignment.score  # Alignment score

        # Calculate the number of matching amino acids
        matching_aa = sum(1 for a, b in zip(aln1, aln2) if a == b)

        mimic_data.append((kp, annexin_peptide, matching_aa, score))
    
    return mimic_data

# Function to select the top 5 matching peptides from Klebsiella for each Annexin peptide
def select_top_mimics_for_each_annexin(annexin_peptides, kleb_peptides, top_n=5):
    all_mimic_data = []

    # For each Annexin peptide, align with all Klebsiella peptides
    for annexin_peptide in annexin_peptides:
        mimic_data = align_peptides(kleb_peptides, annexin_peptide)

        # Sort by the number of matching amino acids and score (in descending order)
        sorted_mimics = sorted(mimic_data, key=lambda x: (x[2], x[3]), reverse=True)
        
        # Select the top N mimics
        top_mimics = sorted_mimics[:top_n]
        
        # Add the results to the list
        all_mimic_data.append((annexin_peptide, top_mimics))

    return all_mimic_data

# Load peptides from files
kleb_peptides = load_peptides("kleb_peptides.txt")
annexin_peptides = load_peptides("annexin_peptides.txt")

# Select top 5 mimics for each Annexin peptide
top_mimics_per_annexin = select_top_mimics_for_each_annexin(annexin_peptides, kleb_peptides, top_n=5)

# Write the results to a file
with open("top_5_mimics_per_annexin.txt", "w") as f:
    f.write("Annexin Peptide\tKlebsiella Peptide\tMatching AA\tScore\n")
    s_no = 1
    for annexin_peptide, top_mimics in top_mimics_per_annexin:
        for kp, ap, matching_aa, score in top_mimics:
            f.write(f"{s_no}\t{annexin_peptide}\t{kp}\t{matching_aa}\t{score}\n")
            s_no += 1

print(f"✅ Done! Top 5 mimicry pairs per Annexin peptide saved in 'top_5_mimics_per_annexin.txt'.")








