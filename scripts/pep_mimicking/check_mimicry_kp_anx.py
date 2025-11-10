# -----------------------------
# Peptide Mimicry Finder
# Compare Klebsiella peptides with human Annexin peptides
# and find similar sequences
# -----------------------------

# Import Biopython tools for sequence alignment
from Bio.Align import PairwiseAligner
from Bio.Align import substitution_matrices

# -----------------------------
# Function to read peptides from a file
# Each peptide should be on a separate line in the text file
# -----------------------------
def load_peptides(file_path):
    with open(file_path, 'r') as f:  # Open file for reading
        # Remove empty lines and extra spaces
        return [line.strip() for line in f if line.strip()]

# -----------------------------
# Function to find mimicry peptides with visual alignment
# -----------------------------
def find_mimics_visual(kp_peptides, anx_peptides, score_threshold=15):
    aligner = PairwiseAligner()  # Create an aligner object
    matrix = substitution_matrices.load("BLOSUM62")  # Load amino acid scoring matrix
    aligner.substitution_matrix = matrix  # Use BLOSUM62 for scoring
    
    mimics = []  # List to store mimicry matches
    s_no = 1    # Serial number for each Annexin peptide

    # Loop through each human peptide
    for ap in anx_peptides:
        # Compare with each Kp peptide
        for kp in kp_peptides:
            alignments = aligner.align(kp, ap)  # Align the two sequences
            best_alignment = alignments[0]      # Pick the best alignment
            aln1, aln2 = best_alignment[:2]     # Get aligned sequences
            score = best_alignment.score         # Get similarity score

            # Only save if score is above threshold
            if score >= score_threshold:
                # Create a line showing matches: "|" if letters match
                match_line = "".join("|" if a == b else " " for a, b in zip(aln1, aln2))
                
                # Combine sequences and match line for visual display
                similarity_format = f"{aln1}\n{match_line}\n{aln2}"
                
                # Save result: serial no, human peptide, bacterial peptide, visual match, score
                mimics.append((s_no, ap, kp, similarity_format, score))

        s_no += 1  # Move to next Annexin peptide

    return mimics  # Return all matches found

# -----------------------------
# Load peptides from files
# -----------------------------
kleb_peptides = load_peptides("kp_peptides.txt")     # Klebsiella peptides
annexin_peptides = load_peptides("anx_peptides.txt")  # Human Annexin peptides

# -----------------------------
# Find mimicry peptides
# -----------------------------
mimics = find_mimics_visual(kp_peptides, anx_peptides, score_threshold=15)

# -----------------------------
# Save results to a text file
# -----------------------------
with open("mimicry_visual_results.txt", "w") as f:
    # Write a header row
    f.write("s.no.\tAnx Peptide\tKp Peptide\tSimilarity\tScore\n")
    # Write each mimicry pair
    for s_no, a1, a2, similarity, score in mimics:
        f.write(f"{s_no}\t{a1}\t{a2}\n{similarity}\t{score}\n")

# Print how many mimicry pairs were found
print(f"✅ Done! {len(mimics)} mimicry pairs saved with visual alignment.")
