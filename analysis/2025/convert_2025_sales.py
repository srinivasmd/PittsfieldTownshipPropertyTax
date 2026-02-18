#!/usr/bin/env python3
"""Convert 2025 Residential Sales Study PDF to CSV using text-based parsing."""
import pdfplumber
import csv
import re
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "2025%20Sales%20Study%20-%20Residential.pdf")
CSV_PATH = os.path.join(os.path.dirname(__file__), "2025_Residential_Sales_Analysis.csv")

def clean_money(val):
    if not val:
        return ""
    return val.replace("$", "").replace(",", "").strip()

def normalize_dashes(s):
    """Replace en-dashes and other dash variants with regular hyphens."""
    return s.replace("\u2010", "-").replace("\u2011", "-").replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")

def parse_data_line(line, current_sub):
    """Parse a data line. 2025 format has fewer columns than 2026 (no Asd_When_Sold, etc.)."""
    m = re.match(r"(L\s*-[\d-]+)\s+(.+)", line)
    if not m:
        return None

    parcel = m.group(1).strip()
    rest = m.group(2).strip()

    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', rest)
    if not date_match:
        return None

    street = rest[:date_match.start()].strip()
    after_date = rest[date_match.end():].strip()
    sale_date = date_match.group(1)

    tokens = after_date.split()
    sale_price = ""
    instr = ""
    terms = ""
    adj_sale = ""
    ecf_area = ""
    other_parcels = ""
    land_table = ""

    i = 0
    if i < len(tokens) and tokens[i].startswith("$"):
        sale_price = tokens[i]
        i += 1

    if i < len(tokens) and tokens[i] in ("WD", "CD", "SD", "PTA", "OTH", "LC", "QC"):
        instr = tokens[i]
        i += 1

    terms_parts = []
    while i < len(tokens) and not tokens[i].startswith("$"):
        if tokens[i].startswith("'"):
            break
        terms_parts.append(tokens[i])
        i += 1
    terms = " ".join(terms_parts)

    if i < len(tokens) and tokens[i].startswith("$"):
        adj_sale = tokens[i]
        i += 1

    if i < len(tokens) and tokens[i].startswith("'"):
        ecf_area = tokens[i].lstrip("'")
        i += 1

    if i < len(tokens) and tokens[i].startswith("L"):
        other_parcels = tokens[i]
        i += 1

    land_table = " ".join(tokens[i:]) if i < len(tokens) else ""

    return {
        "Subdivision": current_sub,
        "Parcel_Number": parcel,
        "Street_Address": street,
        "Sale_Date": sale_date,
        "Sale_Price": clean_money(sale_price),
        "Instr": instr,
        "Terms_of_Sale": terms,
        "Adj_Sale": clean_money(adj_sale),
        "ECF_Area": ecf_area,
        "Other_Parcels_in_Sale": other_parcels,
        "Land_Table": land_table,
    }

def main():
    all_rows = []
    current_sub = ""

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = normalize_dashes(page.extract_text() or "")
            lines = text.split("\n")

            for line in lines:
                ls = line.strip()
                if not ls:
                    continue

                if ls.startswith("Parcel Number") or ls.startswith("Totals:"):
                    continue
                if ls.startswith("Sale. Ratio") or ls.startswith("Std. Dev."):
                    continue
                if "NO SALES" in ls or "NO CHANGE" in ls:
                    continue

                if ls.startswith("L") and re.match(r'L\s*-\d{2}-\d{2}', ls):
                    row = parse_data_line(ls, current_sub)
                    if row:
                        all_rows.append(row)
                    continue

                # Subdivision header: e.g., "AR-2 WOODLANDS ARBOR RIDGE" or "AR-4 MEADOWS OF ARBOR RIDGE"
                sub_match = re.match(r'^([A-Z]{2,5}-?\d*\.?\d*)\s+(.+)', ls)
                if sub_match and not ls.startswith("L"):
                    candidate = sub_match.group(1)
                    name = sub_match.group(2).strip()
                    if (name.isupper() and len(candidate) <= 10 and
                        not any(kw in name for kw in ["PARCEL", "TOTALS", "$", "SALE.", "STD.", "STREET", "TERMS", "INSTR"])):
                        current_sub = f"{candidate} {name}"
                        continue

    fieldnames = ["Subdivision", "Parcel_Number", "Street_Address", "Sale_Date",
                   "Sale_Price", "Instr", "Terms_of_Sale", "Adj_Sale",
                   "ECF_Area", "Other_Parcels_in_Sale", "Land_Table"]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Extracted {len(all_rows)} rows to {CSV_PATH}")

if __name__ == "__main__":
    main()
