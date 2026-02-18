#!/usr/bin/env python3
"""Convert 2024 Residential ECF Analysis PDF to CSV."""
import pdfplumber
import csv
import re
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "Copy%20of%20RES%20ECF%20ANALYSIS%202024%20-%20website_202404090957495714.pdf")
CSV_PATH = os.path.join(os.path.dirname(__file__), "2024_Residential_ECF_Analysis.csv")

def clean_money(val):
    if not val:
        return ""
    return val.replace("$", "").replace(",", "").strip()

def normalize_dashes(s):
    return s.replace("\u2010", "-").replace("\u2011", "-").replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")

def parse_data_line(line, current_sub, current_ecf_area):
    m = re.match(r"(L\s*-[\d-]+)\s+(.+)", line)
    if not m:
        return None
    parcel = m.group(1).strip()
    rest = m.group(2).strip()
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', rest)
    if not date_match:
        return None
    street = rest[:date_match.start()].strip()
    after_date = rest[date_match.end():].strip()
    sale_date = date_match.group(1)
    tokens = after_date.split()

    money_vals = []
    other_vals = []
    building_style = ""
    for t in tokens:
        if t.startswith("$"):
            money_vals.append(t)
        elif re.match(r'[\d.]+$', t):
            other_vals.append(t)
        else:
            building_style = (building_style + " " + t).strip()

    return {
        "Subdivision": current_sub,
        "ECF_Area_Code": current_ecf_area,
        "Parcel_Number": parcel,
        "Street_Address": street,
        "Sale_Date": sale_date,
        "Sale_Price": clean_money(money_vals[0]) if len(money_vals) >= 1 else "",
        "Adj_Sale": clean_money(money_vals[1]) if len(money_vals) >= 2 else "",
        "Land_Value": clean_money(money_vals[2]) if len(money_vals) >= 3 else "",
        "Land_Yard": clean_money(money_vals[3]) if len(money_vals) >= 4 else "",
        "Bldg_Residual": clean_money(money_vals[4]) if len(money_vals) >= 5 else "",
        "Cost_Man": clean_money(money_vals[5]) if len(money_vals) >= 6 else "",
        "ECF": other_vals[-1] if other_vals else "",
        "Building_Style": building_style,
    }

def main():
    all_rows = []
    current_sub = ""
    current_ecf_area = ""
    ecf_summaries = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = normalize_dashes(page.extract_text() or "")
            for line in text.split("\n"):
                ls = line.strip()
                if not ls: continue
                if ls.startswith("Parcel Number") or ls.startswith("Totals:"): continue
                if ls.startswith("E.C.F.") or ls.startswith("Ave. E.C.F."):
                    ecf_match = re.search(r'=>\s*([\d.]+)', ls)
                    if ecf_match and current_ecf_area and ls.startswith("Ave."):
                        ecf_summaries.append({"ECF_Area": current_ecf_area, "Subdivision": current_sub, "Ave_ECF": ecf_match.group(1)})
                    continue
                if ls.startswith("L") and re.match(r'L\s*-\d{2}-\d{2}', ls):
                    row = parse_data_line(ls, current_sub, current_ecf_area)
                    if row: all_rows.append(row)
                    continue
                # Header like "AR-4 - ARBOR RIDGE MEADOWS" or "ARBOR RIDGE -MEADOWS AR-4"
                area_match = re.match(r'^([A-Z]{2,5}-?\d*\.?\d*)\s*-\s*(.+)', ls)
                if area_match:
                    current_ecf_area = area_match.group(1)
                    current_sub = area_match.group(2).strip()
                    continue
                # Alternate format: "ARBOR RIDGE -MEADOWS AR-4"
                alt_match = re.match(r'^(.+?)\s+([A-Z]{2,5}-?\d+)\s*$', ls)
                if alt_match and alt_match.group(1).isupper():
                    current_sub = alt_match.group(1).strip()
                    current_ecf_area = alt_match.group(2).strip()
                    continue
                if "NO CHANGE" in ls: continue
                if ls in ("TWO STORY","TWO-STORY","ONE STORY","ONE-STORY","BI-LEVEL","SPLIT LEVEL","RANCH","COLONIAL"): continue

    fieldnames = ["Subdivision","ECF_Area_Code","Parcel_Number","Street_Address",
                   "Sale_Date","Sale_Price","Adj_Sale","Land_Value","Land_Yard",
                   "Bldg_Residual","Cost_Man","ECF","Building_Style"]
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Extracted {len(all_rows)} rows to {CSV_PATH}")

    summary_path = CSV_PATH.replace(".csv", "_ECF_Summaries.csv")
    if ecf_summaries:
        with open(summary_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["ECF_Area","Subdivision","Ave_ECF"])
            writer.writeheader()
            writer.writerows(ecf_summaries)
        print(f"Wrote {len(ecf_summaries)} ECF summaries to {summary_path}")

if __name__ == "__main__":
    main()
