# 2024 Township Assessment Data

Source: Pittsfield Township Assessing Office (pittsfield-mi.gov)

## Source PDFs

| File | Description |
|------|-------------|
| `2024 Residential Sale Analysis.pdf` | 35 pages, all residential arm's-length sales |
| `Copy of RES ECF ANALYSIS 2024 - website.pdf` | 36 pages, ECF values for all residential areas |
| `2024 Residential Land Analysis.pdf` | 31 pages, land values for all residential areas |

*Note: PDF filenames are URL-encoded (spaces as %20)*

## Generated CSVs

| File | Rows | Description |
|------|------|-------------|
| `2024_Residential_Sales_Analysis.csv` | 1,263 | All sales with parcel, address, date, price, terms, appraisal |
| `2024_Residential_ECF_Analysis.csv` | 851 | Property-level ECF data (sale price vs cost approach) |
| `2024_Residential_ECF_Analysis_ECF_Summaries.csv` | 100 | Average ECF per area code |
| `2024_Residential_Land_Analysis.csv` | 1,120 | Land values, residuals, and allocation ratios |
| `2024_Residential_Land_Analysis_Adjustments.csv` | 81 | Land adjustment factors per area |

## Conversion Scripts

| File | Description |
|------|-------------|
| `convert_2024_sales.py` | PDF -> CSV using pdfplumber text extraction with regex parsing |
| `convert_2024_ecf.py` | PDF -> CSV, handles 2-digit year dates (MM/DD/YY) |
| `convert_2024_land.py` | PDF -> CSV, extracts land values and adjustment factors |

## Usage

Filter any CSV by area code to find data for your subdivision. Area codes (e.g., AR-1, AR-4, AV-1) are listed in the ECF Summaries CSV.
