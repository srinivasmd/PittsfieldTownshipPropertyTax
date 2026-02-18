#!/usr/bin/env python3
"""Convert Residential ECF Analysis 2026 PDF to CSV using text-based parsing."""
import pdfplumber
import csv
import re
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "RESIDENTIAL%20ECF%20ANALYSIS%202026%20-%20WEBSITE.pdf")
CSV_PATH = os.path.join(os.path.dirname(__file__), "2026_Residential_ECF_Analysis.csv")

def clean_money(val):
    if not val:
        return ""
    return val.replace("$", "").replace(",", "").strip()

def parse_data_line(line, current_sub, current_ecf_area):
    """Parse a data line like:
    L -12-13-401-021 4936 MATTHEW CT 10/31/2024 $390,000 $390,000 $81,600 $86,310 $303,690 $219,630 1.383
    """
    m = re.match(r"(L\s*-[\d-]+)\s+(.+)", line)
    if not m:
        return None

    parcel = m.group(1).strip()
    rest = m.group(2).strip()

    # Find the date
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', rest)
    if not date_match:
        return None

    street = rest[:date_match.start()].strip()
    after_date = rest[date_match.end():].strip()
    sale_date = date_match.group(1)

    # After date: Sale_Price Adj_Sale Land_Value Land+Yard Bldg_Residual Cost_Man ECF [Building_Style]
    # All money values start with $, ECF is a decimal
    tokens = after_date.split()

    sale_price = ""
    adj_sale = ""
    land_value = ""
    land_yard = ""
    bldg_residual = ""
    cost_man = ""
    ecf = ""
    building_style = ""

    money_vals = []
    other_vals = []

    for t in tokens:
        if t.startswith("$"):
            money_vals.append(t)
        elif re.match(r'[\d.]+$', t):
            other_vals.append(t)
        else:
            # Could be building style (e.g., "TWO STORY")
            building_style = (building_style + " " + t).strip()

    # Expected order of money values: Sale_Price, Adj_Sale, Land_Value, Land+Yard, Bldg_Residual, Cost_Man
    if len(money_vals) >= 1:
        sale_price = money_vals[0]
    if len(money_vals) >= 2:
        adj_sale = money_vals[1]
    if len(money_vals) >= 3:
        land_value = money_vals[2]
    if len(money_vals) >= 4:
        land_yard = money_vals[3]
    if len(money_vals) >= 5:
        bldg_residual = money_vals[4]
    if len(money_vals) >= 6:
        cost_man = money_vals[5]

    # ECF is the last numeric value (decimal like 1.383 or 0.802)
    if other_vals:
        ecf = other_vals[-1]

    return {
        "Subdivision": current_sub,
        "ECF_Area_Code": current_ecf_area,
        "Parcel_Number": parcel,
        "Street_Address": street,
        "Sale_Date": sale_date,
        "Sale_Price": clean_money(sale_price),
        "Adj_Sale": clean_money(adj_sale),
        "Land_Value": clean_money(land_value),
        "Land_Yard": clean_money(land_yard),
        "Bldg_Residual": clean_money(bldg_residual),
        "Cost_Man": clean_money(cost_man),
        "ECF": ecf,
        "Building_Style": building_style,
    }

def main():
    all_rows = []
    current_sub = ""
    current_ecf_area = ""
    ecf_summaries = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.split("\n")

            for line in lines:
                ls = line.strip()
                if not ls:
                    continue

                # Skip headers and summaries
                if ls.startswith("Parcel Number"):
                    continue
                if ls.startswith("Totals:"):
                    continue
                if ls.startswith("E.C.F.") or ls.startswith("Ave. E.C.F."):
                    # Capture ECF summary
                    ecf_match = re.search(r'=>\s*([\d.]+)', ls)
                    if ecf_match and current_ecf_area:
                        if ls.startswith("Ave."):
                            ecf_summaries.append({
                                "ECF_Area": current_ecf_area,
                                "Subdivision": current_sub,
                                "Ave_ECF": ecf_match.group(1)
                            })
                    continue

                # Data row
                if ls.startswith("L") and re.match(r'L\s*-\d{2}-\d{2}', ls):
                    row = parse_data_line(ls, current_sub, current_ecf_area)
                    if row:
                        all_rows.append(row)
                    continue

                # Check for area code header like "AR-1 - ARBOR RIDGE"
                area_match = re.match(r'^([A-Z]{2,}-?\d*\.?\d*)\s*-\s*(.+)', ls)
                if area_match:
                    current_ecf_area = area_match.group(1)
                    current_sub = area_match.group(2).strip()
                    continue

                # NO CHANGE lines
                if "NO CHANGE" in ls:
                    continue

                # Building style headers (TWO STORY, ONE STORY, etc.)
                if ls in ("TWO STORY", "ONE STORY", "BI-LEVEL", "SPLIT LEVEL", "RANCH", "COLONIAL"):
                    continue

    fieldnames = ["Subdivision", "ECF_Area_Code", "Parcel_Number", "Street_Address",
                   "Sale_Date", "Sale_Price", "Adj_Sale", "Land_Value", "Land_Yard",
                   "Bldg_Residual", "Cost_Man", "ECF", "Building_Style"]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Extracted {len(all_rows)} rows to {CSV_PATH}")

    # Also write ECF summaries
    summary_path = CSV_PATH.replace(".csv", "_ECF_Summaries.csv")
    if ecf_summaries:
        with open(summary_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["ECF_Area", "Subdivision", "Ave_ECF"])
            writer.writeheader()
            writer.writerows(ecf_summaries)
        print(f"Wrote {len(ecf_summaries)} ECF summaries to {summary_path}")

if __name__ == "__main__":
    main()
