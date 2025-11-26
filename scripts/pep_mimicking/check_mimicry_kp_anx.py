# -----------------------------
# The script will help to find mimicry peptide it will compare the Klebsiella (kp) peps with human Annexin peps (anx) and find similar sequences
# -----------------------------

# To import Biopython tools for sequence alignment, the Biopython will function to aligning sequences of both peps and give scores to similarity
from Bio.Align import PairwiseAligner
from Bio.Align import substitution_matrices

# -----------------------------
# This is the function line which explains python how to load peptides from a file when given, it does not load anything right now (it only teaches Python what to do when we later give command to load the file
def load_peptides(file_path):        # tells how to give command to load peps later
    with open(file_path, 'r') as f:   # it will open the file present in path on read mode (keep each peps on a separate line in the text file)
        return [line.strip() for line in f if line.strip()]  # #it will Remove empty lines and extra spaces if any present

# -----------------------------
# this is another function line which tells how to do compare peps
# -----------------------------
def find_mimics_visual(kp_peptides, anx_peptides, score_threshold=15):              # it compares every Anx peps with Kp peps on visual alignment basis, align them, calculate similarity score & keep only the peps has similarity scores above 15 (threshold can be change)
    aligner = PairwiseAligner()     # creates a sequence alignment tool inside Python just like BLAST but much smaller.
    matrix = substitution_matrices.load("BLOSUM62")     # Load amino acid scoring matrix
    aligner.substitution_matrix = matrix    # Use BLOSUM62 for scoring which tells the computer which amino acids are similar
    
    mimics = []  # List to store mimicry matches
    s_no = 1    # Serial number for each Anx peps

    for anx in anx_peptides:
        # loop over anx peps and compare with each Kp peptide
        for kp in kp_peptides:
            alignments = aligner.align(kp, anx)  # Align the two sequences
            best_alignment = alignments[0]      # Pick the best alignment
            aln1, aln2 = best_alignment[:2]     # Get aligned sequences
            score = best_alignment.score         # Get similarity score

            # Only save if score is above threshold
            if score >= score_threshold:
                # Create a line showing matches: "|" if letters match
                match_line = "".join("|" if a == b else " " for a, b in zip(aln1, aln2))
                
                # Combine sequences and match line for visual display
                similarity_format = f"{aln1}\n{match_line}\n{aln2}" 
                
                # Save result in table with coloumns: serial no, human peptide, bacterial peptide, visual match, score
                mimics.append((s_no, ap, kp, similarity_format, score))

        s_no += 1  # Move to next Annexin peptide

    return mimics  # Return all matches found

# -----------------------------
# Load peptides from files
# -----------------------------
kp_peps = load_peptides("kp_peptides.txt")     # Kp peps
anx_peps = load_peptides("anx_peptides.txt")  # anx peps

# -----------------------------
# Find mimicry peptides
# -----------------------------
mimics = find_mimics_visual(kp_peptides, anx_peptides, score_threshold=15)

# -----------------------------
# Save results to a text file in writing mode
# -----------------------------
with open("mimicry_visual_results.txt", "w") as f:
    # Write a header row
    f.write("s.no.\tAnx Peptide\tKp Peptide\tSimilarity\tScore\n")
    # Write each mimicry pair
    for s_no, a1, a2, similarity, score in mimics:
        f.write(f"{s_no}\t{a1}\t{a2}\n{similarity}\t{score}\n")

# Print how many mimicry pairs were found
print(f"✅ Done! {len(mimics)} mimicry pairs saved.")
