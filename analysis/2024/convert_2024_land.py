#!/usr/bin/env python3
"""Convert 2024 Residential Land Analysis PDF to CSV."""
import pdfplumber
import csv
import re
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "2024%20Residential%20Land%20Analysis.pdf")
CSV_PATH = os.path.join(os.path.dirname(__file__), "2024_Residential_Land_Analysis.csv")

def clean_money(val):
    if not val:
        return ""
    return val.replace("$", "").replace(",", "").strip()

def normalize_dashes(s):
    return s.replace("\u2010", "-").replace("\u2011", "-").replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")

def parse_data_line(line, current_sub, current_area_code, current_avg_land):
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

    sale_price = ""; terms = ""; adj_sale = ""; land_residual = ""
    land_value_prev = ""; ratio = ""; adj_land = ""; land_value_2024 = ""
    adj_alloc = ""; acres = ""; ecf_area = ""; land_table = ""
    cls = ""; rate_group = ""

    i = 0
    if i < len(tokens) and tokens[i].startswith("$"):
        sale_price = tokens[i]; i += 1
    terms_parts = []
    while i < len(tokens) and not tokens[i].startswith("$"):
        if tokens[i].startswith("'"): break
        terms_parts.append(tokens[i]); i += 1
    terms = " ".join(terms_parts)
    if i < len(tokens) and tokens[i].startswith("$"):
        adj_sale = tokens[i]; i += 1
    if i < len(tokens) and tokens[i].startswith("$"):
        land_residual = tokens[i]; i += 1
    if i < len(tokens) and tokens[i].startswith("$"):
        land_value_prev = tokens[i]; i += 1
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        ratio = tokens[i]; i += 1
    if i < len(tokens) and (tokens[i].startswith("$") or re.match(r'[\d,]+$', tokens[i])):
        adj_land = tokens[i]; i += 1
    if i < len(tokens) and (tokens[i].startswith("$") or re.match(r'[\d,]+$', tokens[i])):
        land_value_2024 = tokens[i]; i += 1
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        adj_alloc = tokens[i]; i += 1
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        acres = tokens[i]; i += 1
    if i < len(tokens) and (tokens[i].startswith("'") or re.match(r'^[A-Z]{2,}-?\d', tokens[i])):
        ecf_area = tokens[i].lstrip("'"); i += 1
    land_table_parts = []
    while i < len(tokens):
        if re.match(r'^\d{3}$', tokens[i]):
            cls = tokens[i]; i += 1; break
        land_table_parts.append(tokens[i]); i += 1
    land_table = " ".join(land_table_parts)
    if not cls and i < len(tokens) and re.match(r'^\d{3}$', tokens[i]):
        cls = tokens[i]; i += 1
    if i < len(tokens):
        rate_group = " ".join(tokens[i:])

    return {
        "Subdivision": current_sub, "Area_Code": current_area_code,
        "Avg_Land_Value": current_avg_land, "Parcel_Number": parcel,
        "Street_Address": street, "Sale_Date": sale_date,
        "Sale_Price": clean_money(sale_price), "Terms_of_Sale": terms,
        "Adj_Sale": clean_money(adj_sale), "Land_Residual": clean_money(land_residual),
        "Land_Value_2023": clean_money(land_value_prev), "Ratio_LV_SP": ratio,
        "Adj_Land_Value": clean_money(adj_land),
        "Land_Value_2024": land_value_2024.replace(",","").replace("$",""),
        "Adj_Alloc_Ratio_LV_SP": adj_alloc, "Total_Acres": acres,
        "ECF_Area": ecf_area, "Land_Table": land_table,
        "Class": cls, "Rate_Group": rate_group,
    }

def main():
    all_rows = []
    current_sub = ""; current_area_code = ""; current_avg_land = ""
    land_adjustments = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page in pdf.pages:
            text = normalize_dashes(page.extract_text() or "")
            for line in text.split("\n"):
                ls = line.strip()
                if not ls: continue
                if ls.startswith("Parcel Number") or ls.startswith("Totals:"): continue
                adjust_match = re.match(r'([\d.]+)\s*ADJUST\s+2023\s+LAND\s+VALUE\s+BY', ls)
                if adjust_match:
                    land_adjustments.append({"Area_Code": current_area_code, "Subdivision": current_sub, "Adjust_Factor": adjust_match.group(1)})
                    continue
                if ls.startswith("L") and re.match(r'L\s*-\d{2}-\d{2}', ls):
                    row = parse_data_line(ls, current_sub, current_area_code, current_avg_land)
                    if row: all_rows.append(row)
                    continue
                header_match = re.match(r'^(.+?)\s+([A-Z]{2,5}-?\d*\.?\d*)\s+(?:AVERAGE\s+\$?([\d,]+)|NO\s+CHANGE)', ls)
                if header_match and not ls.startswith("L"):
                    sub_name = header_match.group(1).strip()
                    area_code = header_match.group(2).strip()
                    avg_land = header_match.group(3) or ""
                    if len(area_code) <= 10 and sub_name.isupper():
                        current_sub = sub_name
                        current_area_code = area_code
                        current_avg_land = avg_land.replace(",","")
                        continue

    fieldnames = ["Subdivision","Area_Code","Avg_Land_Value","Parcel_Number","Street_Address",
                   "Sale_Date","Sale_Price","Terms_of_Sale","Adj_Sale",
                   "Land_Residual","Land_Value_2023","Ratio_LV_SP",
                   "Adj_Land_Value","Land_Value_2024","Adj_Alloc_Ratio_LV_SP",
                   "Total_Acres","ECF_Area","Land_Table","Class","Rate_Group"]
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Extracted {len(all_rows)} rows to {CSV_PATH}")

    adj_path = CSV_PATH.replace(".csv", "_Adjustments.csv")
    if land_adjustments:
        with open(adj_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Area_Code","Subdivision","Adjust_Factor"])
            writer.writeheader()
            writer.writerows(land_adjustments)
        print(f"Wrote {len(land_adjustments)} adjustments to {adj_path}")

if __name__ == "__main__":
    main()
