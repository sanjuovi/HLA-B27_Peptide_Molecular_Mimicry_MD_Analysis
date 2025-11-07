from Bio.Align import PairwiseAligner
from Bio.Align import substitution_matrices

def load_peptides(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def find_mimics_visual(kleb_peptides, annexin_peptides, score_threshold=15):
    aligner = PairwiseAligner()
    matrix = substitution_matrices.load("BLOSUM62")  # Load BLOSUM62 matrix

    aligner.substitution_matrix = matrix
    mimics = []
    s_no = 1  # Serial number counter for each Annexin peptide

    for ap in annexin_peptides:
        for kp in kleb_peptides:
            # Perform global alignment
            alignments = aligner.align(kp, ap)
            best_alignment = alignments[0]  # Get the best alignment
            aln1, aln2 = best_alignment[:2]  # Aligned sequences
            score = best_alignment.score  # Alignment score

            if score >= score_threshold:
                # Build match line for visual representation
                match_line = "".join("|" if a == b else " " for a, b in zip(aln1, aln2))
                
                # Create the neatly formatted output for similarity column
                similarity_format = f"{aln1}\n{match_line}\n{aln2}"
                
                mimics.append((s_no, ap, kp, similarity_format, score))

        s_no += 1  # Increment the serial number after each Annexin peptide

    return mimics

# Load peptides from the respective files
kleb_peptides = load_peptides("kleb_peptides.txt")
annexin_peptides = load_peptides("annexin_peptides.txt")

# Find mimics with visual alignment
mimics = find_mimics_visual(kleb_peptides, annexin_peptides, score_threshold=15)

# Save results to a file in the desired format
with open("mimicry_visual_results.txt", "w") as f:
    f.write("s.no.\tAnnexin Peptide\tKlebsiella Peptide\tSimilarity\tScore\n")
    for s_no, a1, a2, similarity, score in mimics:
        f.write(f"{s_no}\t{a1}\t{a2}\n{similarity}\t{score}\n")

print(f"✅ Done! {len(mimics)} mimicry pairs saved with visual alignment.")




