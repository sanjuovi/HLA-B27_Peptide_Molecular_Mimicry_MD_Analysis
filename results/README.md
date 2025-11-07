# ✅ MD Simulation Results Summary

This folder contains the molecular dynamics (MD) simulation outputs for the **Annexin peptide (ANX)** and three **Klebsiella pneumoniae peptides (KP1, KP2, KP3)**, each bound to the HLA protein.

The simulations were performed for **1 μs** using **GROMACS 2023** on the **DelftBlue Supercomputer**, after system preparation and optimization using **AmberTools23**.

---

### 📁 Folder Structure

results/
│── README.md
│── summary_table/        # Mean ± SD values for each MD metric
│   ├── all_properties_summary.csv
│   └── all_properties_summary.xlsx
│
└── plots/                # Combined comparison plots
    ├── RMSD/
    ├── RMSF/
    ├── RGYR/
    ├── SASA/
    ├── HBond/
    ├── MMGBSA/
    └── Hydrophobicity/

Each subfolder contains one combined plot comparing **ANX, KP1, KP2, KP3**.

---

### 📊 Supporting Plots (what each shows)

| Folder | Description |
|--------|-------------|
| `RMSD/` | Backbone stability of all complexes |
| `RMSF/` | Flexibility of peptide residues |
| `RGYR/` | Compactness (radius of gyration) |
| `SASA/` | Solvent accessibility of peptide |
| `HBond/` | Hydrogen bonds over simulation time |
| `MMGBSA/` | Binding free energy comparison |
| `Hydrophobicity/` | Hydrophobic interactions comparison |

---

### ✅ Summary Table

The **summary_table/** folder contains calculated **mean ± standard deviation** values for:
RMSD, RMSF, Rg, SASA, Hydrogen bonds, MMGBSA energy.
Values were extracted from `.xvg` analysis files for each system.

---

### 🔍 Key Observations

- **ANX (human peptide)** showed the **highest stability and most compact conformation** (lowest RMSD & Rg, highest H-bond count)
- **KP1** behaved most similar to ANX across multiple metrics and is the **strongest mimicry candidate**
- **KP2** had high flexibility (high RMSF) and weak binding energy (less stable)
- **KP3** was intermediate in stability and interaction strength

---

✅ **Conclusion:**  
Among tested Klebsiella peptides, **KP1 is the most likely molecular mimic** of the human Annexin peptide in HLA binding.

---

### ✅ Why this matters

A microbial peptide that behaves structurally like the self-peptide may trigger **cross-reactive immune responses**, helping explain molecular mimicry in autoimmune pathways.

---
