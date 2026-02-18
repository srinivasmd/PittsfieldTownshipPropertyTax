#!/usr/bin/env python3
"""Convert 2026 Residential Sales Analysis PDF to CSV using text-based parsing."""
import pdfplumber
import csv
import re
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "2026%20RESIDENTIAL%20SALES%20ANALYSIS.pdf")
CSV_PATH = os.path.join(os.path.dirname(__file__), "2026_Residential_Sales_Analysis.csv")

def clean_money(val):
    if not val:
        return ""
    return val.replace("$", "").replace(",", "").strip()

def parse_data_line(line, current_sub):
    """Parse a data line like:
    L -12-13-401-009 4562 CHRISTINA DR 8/2/2024 $355,000 WD 03-ARM'S LENGTH $355,000 $161,432 45.47 $389,440 'AR-1 AR1-ARBOR RIDGE
    """
    # Match parcel number at start
    m = re.match(r"(L\s*-[\d-]+)\s+(.+)", line)
    if not m:
        return None

    parcel = m.group(1).strip()
    rest = m.group(2).strip()

    # Find the date (MM/DD/YYYY)
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', rest)
    if not date_match:
        return None

    street = rest[:date_match.start()].strip()
    after_date = rest[date_match.end():].strip()
    sale_date = date_match.group(1)

    # After date: Sale_Price Instr Terms Adj_Sale Asd_When_Sold Asd/Adj_Sale Cur_Appraisal ECF_Area Land_Table
    # Pattern: $355,000 WD 03-ARM'S LENGTH $355,000 $161,432 45.47 $389,440 'AR-1 AR1-ARBOR RIDGE

    # Extract money values and other tokens
    # First token should be sale price
    tokens = after_date.split()

    sale_price = ""
    instr = ""
    terms = ""
    adj_sale = ""
    asd_when_sold = ""
    asd_adj_sale = ""
    cur_appraisal = ""
    ecf_area = ""
    land_table = ""

    i = 0
    # Sale price (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        sale_price = tokens[i]
        i += 1

    # Instrument (WD, CD, etc.)
    if i < len(tokens) and tokens[i] in ("WD", "CD", "SD", "PTA", "OTH", "LC"):
        instr = tokens[i]
        i += 1

    # Terms of sale - collect until we hit a $ value
    terms_parts = []
    while i < len(tokens) and not tokens[i].startswith("$"):
        # Check if this looks like it could be an ECF area code
        if tokens[i].startswith("'"):
            break
        terms_parts.append(tokens[i])
        i += 1
    terms = " ".join(terms_parts)

    # Adj Sale (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        adj_sale = tokens[i]
        i += 1

    # Asd when sold (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        asd_when_sold = tokens[i]
        i += 1

    # Asd/Adj Sale ratio (numeric like 45.47)
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        asd_adj_sale = tokens[i]
        i += 1

    # Cur Appraisal (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        cur_appraisal = tokens[i]
        i += 1

    # ECF Area (starts with ')
    if i < len(tokens) and tokens[i].startswith("'"):
        ecf_area = tokens[i].lstrip("'")
        i += 1

    # Other parcels (starts with L-)
    other_parcels = ""
    if i < len(tokens) and tokens[i].startswith("L"):
        other_parcels = tokens[i]
        i += 1

    # Land table (remaining)
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
        "Asd_When_Sold": clean_money(asd_when_sold),
        "Asd_Adj_Sale": asd_adj_sale,
        "Cur_Appraisal": clean_money(cur_appraisal),
        "ECF_Area": ecf_area,
        "Other_Parcels_in_Sale": other_parcels,
        "Land_Table": land_table,
    }

def main():
    all_rows = []
    current_sub = ""

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.split("\n")

            for line in lines:
                ls = line.strip()
                if not ls:
                    continue

                # Skip headers and summary rows
                if ls.startswith("Parcel Number") or ls.startswith("Totals:"):
                    continue
                if ls.startswith("Sale. Ratio") or ls.startswith("Std. Dev."):
                    continue
                if "NO SALES" in ls or "NO CHANGE" in ls:
                    continue

                # Data row - starts with L and has parcel pattern
                if ls.startswith("L") and re.match(r'L\s*-\d{2}-\d{2}', ls):
                    row = parse_data_line(ls, current_sub)
                    if row:
                        all_rows.append(row)
                    continue

                # Subdivision header: all caps, longer than 3 chars, not a data/header line
                if (ls.isupper() and len(ls) > 3 and
                    not any(kw in ls for kw in ["PARCEL", "TOTALS", "$", "SALE.", "STD.",
                                                 "ADJ.", "CUR.", "STREET", "TERMS", "INSTR",
                                                 "ASD", "ECF", "LAND"])):
                    current_sub = ls

    fieldnames = ["Subdivision", "Parcel_Number", "Street_Address", "Sale_Date",
                   "Sale_Price", "Instr", "Terms_of_Sale", "Adj_Sale",
                   "Asd_When_Sold", "Asd_Adj_Sale", "Cur_Appraisal",
                   "ECF_Area", "Other_Parcels_in_Sale", "Land_Table"]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Extracted {len(all_rows)} rows to {CSV_PATH}")

if __name__ == "__main__":
    main()
