# 2026 Township Assessment Data

Source: Pittsfield Township Assessing Office (pittsfield-mi.gov)

## Source PDFs

| File | Description |
|------|-------------|
| `2026 RESIDENTIAL SALES ANALYSIS.pdf` | 40 pages, all residential arm's-length sales |
| `RESIDENTIAL ECF ANALYSIS 2026 - WEBSITE.pdf` | 48 pages, ECF values for all residential areas |
| `RESIDENTIAL LAND ANALYSIS 2026.pdf` | 36 pages, land values for all residential areas |

*Note: PDF filenames are URL-encoded (spaces as %20)*

## Generated CSVs

| File | Rows | Description |
|------|------|-------------|
| `2026_Residential_Sales_Analysis.csv` | 803 | All sales with parcel, address, date, price, terms, appraisal |
| `2026_Residential_ECF_Analysis.csv` | 660 | Property-level ECF data (sale price vs cost approach) |
| `2026_Residential_ECF_Analysis_ECF_Summaries.csv` | 88 | Average ECF per area code |
| `2026_Residential_Land_Analysis.csv` | 742 | Land values, residuals, and allocation ratios |
| `2026_Residential_Land_Analysis_Adjustments.csv` | 82 | Land adjustment factors per area |

## Conversion Scripts

| File | Description |
|------|-------------|
| `convert_sales_analysis.py` | PDF -> CSV using pdfplumber text extraction with regex parsing |
| `convert_ecf_analysis.py` | PDF -> CSV for ECF data and area summaries |
| `convert_land_analysis.py` | PDF -> CSV for land values and adjustment factors |

## Usage

Filter any CSV by area code to find data for your subdivision. Area codes (e.g., AR-1, AR-4, AV-1) are listed in the ECF Summaries CSV.
