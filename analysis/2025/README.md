# 2025 Township Assessment Data

Source: Pittsfield Township Assessing Office (pittsfield-mi.gov)

## Source PDFs

| File | Description |
|------|-------------|
| `2025 Residential ECF analysis.pdf` | 42 pages, ECF values for all residential areas |
| `2025 Residential Land analysis.pdf` | 36 pages, land values for all residential areas |
| `2025 Sales Study - Residential.pdf` | 34 pages, all residential arm's-length sales |

*Note: PDF filenames are URL-encoded (spaces as %20). 2025 PDFs use Unicode en-dashes instead of ASCII hyphens -- conversion scripts handle this automatically.*

## Generated CSVs

| File | Rows | Description |
|------|------|-------------|
| `2025_Residential_Sales_Analysis.csv` | 972 | All sales with parcel, address, date, price, terms |
| `2025_Residential_ECF_Analysis.csv` | 800 | Property-level ECF data (sale price vs cost approach) |
| `2025_Residential_ECF_Analysis_ECF_Summaries.csv` | 99 | Average ECF per area code |
| `2025_Residential_Land_Analysis.csv` | 912 | Land values, residuals, and allocation ratios |
| `2025_Residential_Land_Analysis_Adjustments.csv` | 86 | Land adjustment factors per area |

## Conversion Scripts

| File | Description |
|------|-------------|
| `convert_2025_sales.py` | PDF -> CSV with `normalize_dashes()` for en-dash handling |
| `convert_2025_ecf.py` | PDF -> CSV with dash normalization |
| `convert_2025_land.py` | PDF -> CSV, references 2024 land values |

## Usage

Filter any CSV by area code to find data for your subdivision. Area codes (e.g., AR-1, AR-4, AV-1) are listed in the ECF Summaries CSV.
