# Fieldcrest Ln / University Palisades (UNF) Analysis

Analysis and appeal documents specific to 3543 Fieldcrest Ln in the University Palisades subdivision (UNF), Pittsfield Township.

## Files

| File | Description |
|------|-------------|
| `2026_Comprehensive_Tax_Appeal_Analysis.md` | Full analysis in markdown format |
| `2026_Comprehensive_Tax_Appeal_Analysis.pdf` | Same analysis as shareable PDF |
| `Property_Tax_Appeal_Guide_Fieldcrest_Ln.docx` | Pre-filled Word appeal guide for 3543 Fieldcrest Ln |
| `generate_analysis_pdf.py` | Script to regenerate the analysis PDF |
| `generate_appeal_guide.py` | Script to regenerate the Word appeal guide |

## UNF Key Findings

- **2026 SEV:** $253,427 → Implied TCV: **$506,854**
- **Taxable Value:** $201,370
- **Implied TCV exceeds every sale** in University Palisades — highest ever was $470,000
- **Fieldcrest Ln average:** $445,800 (assessment is $61,054 / 13.7% above)
- **ECF trend:** 0.974 (2025) → 1.016 (2026) — but individual Fieldcrest Ln ECFs as low as 0.856
- **Recommended SEV:** $215,000–$222,900 (reduction of $30,527–$38,427)

## How to Use

1. Review `2026_Comprehensive_Tax_Appeal_Analysis.pdf` for the full evidence
2. Print `Property_Tax_Appeal_Guide_Fieldcrest_Ln.docx` to submit with your appeal
3. Complete Form L-4035 and submit by **March 10, 2026 at 5:00 PM**
4. If denied, file with Michigan Tax Tribunal by July 31, 2026

## Acronyms

| Acronym | Expansion |
|---------|-----------|
| **UNF** | University Palisades (township subdivision code) |
| **SEV** | State Equalized Value (= 50% of True Cash Value) |
| **TCV** | True Cash Value (= SEV × 2; the "usual selling price") |
| **TV** | Taxable Value (capped annually by Proposal A) |
| **AV** | Assessed Value (same as SEV unless equalization adjusts it) |
| **ECF** | Economic Condition Factor (ratio of sale price to cost-approach value) |
| **PRE** | Principal Residence Exemption (homestead exemption) |
| **CPI** | Consumer Price Index (used for Proposal A TV cap) |
| **BSA** | BS&A Software (township property records system) |
| **MCL** | Michigan Compiled Laws |

## Regenerating Documents

```bash
python generate_analysis_pdf.py   # regenerates the PDF
python generate_appeal_guide.py   # regenerates the Word guide
```

