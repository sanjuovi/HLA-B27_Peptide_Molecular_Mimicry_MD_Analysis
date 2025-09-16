# HLA-B27_Peptide_Molecular_Mimicry_MD_Analysis
 Molecular Dynamics simulations analysis of  human protein HLA-B27:05 (PDB 5txs) to some peptide sequences associated with host protein Annexine and Gut Microbiota (Klebsiella pneumoniae) to identify microbe derived peptides that mimic host peptides in binding behavior to providing insights into molecular mimicry in autoimmune disease such as Ankylosing spondylitis.
 
## Project Overview
This repository contains the molecular dynamics (MD) simulation data, analysis scripts, and results for the study. The goal of this project is to identify pathogen-derived microbe peptides that mimic host-derived ANX peptides in their binding to HLA-B27:05, potentially contributing to molecular mimicry-driven immune activation.

## Methods Summary

Protein Target: HLA-B27:05 (PDB: 5txs)
  - Peptides Studied:
     Host peptide  - Annexine (Anx 1:
     Gut Microbe - Klebsiella pneumoniae: KLEB12, KLEB5, KLEB6, KLEB4, KLEB7
  - Simulation Software: GROMACS 2024
  - Force Field: ff14SB
  - Solvent Model: TIP3P
  - Simulation Length: 1 μs per peptide complex
  - Parameters: 300 K, 1 bar, PME electrostatics, LINCS constraints

---

## 📊 Key Results

| Peptide | Origin | RMSD (nm) | RMSF (nm) | Rg (nm) | H-Bonds | SASA (nm²) | Salt Bridges | Conclusion |
|---------|--------|-----------|-----------|---------|---------|------------|--------------|------------|
| ANX3    | ANX    | 0.25–0.35 | 0.2–0.3   | 2.4–2.6 | High    | ~170–175   | Stable       | Strong/stable binder |
| ANX4    | ANX    | 0.25–0.3  | 0.2–0.3   | ~2.5    | High    | ~170       | Stable       | Outlier in dynamics |
| ANX9    | ANX    | ~0.3      | ~0.3      | ~2.6    | High    | ~175       | Stable       | Good stability |
| KLEB12  | KLEB   | 0.3–0.4   | ~0.3      | 2.5–2.6 | Mod–high| ~175–180   | Stable       | Most ANX-like |
| KLEB5   | KLEB   | 0.5–0.6   | 0.35–0.5  | 2.6–2.8 | Low     | ~190       | Unstable     | Weak binder |
| KLEB6   | KLEB   | ~0.6      | High      | >2.8    | Low     | ~190       | Unstable     | Weakest binder |
| KLEB4   | KLEB   | Moderate  | Moderate  | Slightly high | Moderate | ~180 | Less consistent | Partial mimic |
| KLEB7   | KLEB   | Moderate  | High      | Variable | Low     | High       | Weak         | Poor binder |

**Main conclusion:**  
KLEB12 is the most similar to stable ANX peptides in all MD metrics and is a potential molecular mimic.
