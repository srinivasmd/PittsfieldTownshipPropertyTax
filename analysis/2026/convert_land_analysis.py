#!/usr/bin/env python3
"""Convert Residential Land Analysis 2026 PDF to CSV using text-based parsing."""
import pdfplumber
import csv
import re
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "RESIDENTIAL%20LAND%20ANALYSIS%202026.pdf")
CSV_PATH = os.path.join(os.path.dirname(__file__), "2026_Residential_Land_Analysis.csv")

def clean_money(val):
    if not val:
        return ""
    return val.replace("$", "").replace(",", "").strip()

def parse_data_line(line, current_sub, current_area_code, current_avg_land):
    """Parse a data line like:
    L -12-13-401-009 4562 CHRISTINA DR 8/2/2024 $355,000 03-ARM'S LENGTH $355,000 $107,950 $81,000 0.23 $81,575 81,600 0.23 0.20 'AR-1 AR1-ARBOR RIDGE 401 AVERAGE
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

    # After date: Sale_Price Terms Adj_Sale Land_Residual 2025_Land_Value Ratio Adj_Land_Value 2026_Land_Value Adj_Alloc_Ratio Total_Acres ECF_Area Land_Table Class Rate_Group
    tokens = after_date.split()

    sale_price = ""
    terms = ""
    adj_sale = ""
    land_residual = ""
    land_value_2025 = ""
    ratio_lv_sp = ""
    adj_land_value = ""
    land_value_2026 = ""
    adj_alloc_ratio = ""
    total_acres = ""
    ecf_area = ""
    land_table = ""
    cls = ""
    rate_group = ""

    i = 0

    # Sale price (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        sale_price = tokens[i]
        i += 1

    # Terms of sale - collect until we hit $ value
    terms_parts = []
    while i < len(tokens) and not tokens[i].startswith("$"):
        if tokens[i].startswith("'"):
            break
        terms_parts.append(tokens[i])
        i += 1
    terms = " ".join(terms_parts)

    # Adj Sale (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        adj_sale = tokens[i]
        i += 1

    # Land Residual (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        land_residual = tokens[i]
        i += 1

    # 2025 Land Value (starts with $)
    if i < len(tokens) and tokens[i].startswith("$"):
        land_value_2025 = tokens[i]
        i += 1

    # Ratio LV/SP (decimal)
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        ratio_lv_sp = tokens[i]
        i += 1

    # Adj Land Value (could start with $ or be plain number)
    if i < len(tokens):
        if tokens[i].startswith("$"):
            adj_land_value = tokens[i]
            i += 1
        elif re.match(r'[\d,]+$', tokens[i]):
            adj_land_value = tokens[i]
            i += 1

    # 2026 Land Value (plain number like 81,600 or 81600)
    if i < len(tokens) and re.match(r'[\d,]+$', tokens[i]):
        land_value_2026 = tokens[i]
        i += 1

    # Adj Alloc Ratio (decimal)
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        adj_alloc_ratio = tokens[i]
        i += 1

    # Total Acres (decimal)
    if i < len(tokens) and re.match(r'[\d.]+$', tokens[i]):
        total_acres = tokens[i]
        i += 1

    # ECF Area (starts with ')
    if i < len(tokens) and tokens[i].startswith("'"):
        ecf_area = tokens[i].lstrip("'")
        i += 1
    # Sometimes ECF area doesn't have quote prefix
    elif i < len(tokens) and re.match(r"^[A-Z]{2,}-?\d", tokens[i]):
        ecf_area = tokens[i]
        i += 1

    # Land Table (e.g., AR1-ARBOR RIDGE)
    land_table_parts = []
    while i < len(tokens):
        t = tokens[i]
        if re.match(r'^\d{3}$', t):  # Class like 401
            cls = t
            i += 1
            break
        land_table_parts.append(t)
        i += 1
    land_table = " ".join(land_table_parts)

    # If class wasn't found yet
    if not cls and i < len(tokens) and re.match(r'^\d{3}$', tokens[i]):
        cls = tokens[i]
        i += 1

    # Rate group (remaining)
    if i < len(tokens):
        rate_group = " ".join(tokens[i:])

    return {
        "Subdivision": current_sub,
        "Area_Code": current_area_code,
        "Avg_Land_Value": current_avg_land,
        "Parcel_Number": parcel,
        "Street_Address": street,
        "Sale_Date": sale_date,
        "Sale_Price": clean_money(sale_price),
        "Terms_of_Sale": terms,
        "Adj_Sale": clean_money(adj_sale),
        "Land_Residual": clean_money(land_residual),
        "Land_Value_2025": clean_money(land_value_2025),
        "Ratio_LV_SP": ratio_lv_sp,
        "Adj_Land_Value": clean_money(adj_land_value),
        "Land_Value_2026": land_value_2026.replace(",", ""),
        "Adj_Alloc_Ratio_LV_SP": adj_alloc_ratio,
        "Total_Acres": total_acres,
        "ECF_Area": ecf_area,
        "Land_Table": land_table,
        "Class": cls,
        "Rate_Group": rate_group,
    }

def main():
    all_rows = []
    current_sub = ""
    current_area_code = ""
    current_avg_land = ""
    land_adjustments = []

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

                # Capture adjustment factor
                adjust_match = re.match(r'([\d.]+)\s*ADJUST\s+2025\s+LAND\s+VALUE\s+BY', ls)
                if adjust_match:
                    land_adjustments.append({
                        "Area_Code": current_area_code,
                        "Subdivision": current_sub,
                        "Adjust_Factor": adjust_match.group(1)
                    })
                    continue

                # Data row
                if ls.startswith("L") and re.match(r'L\s*-\d{2}-\d{2}', ls):
                    row = parse_data_line(ls, current_sub, current_area_code, current_avg_land)
                    if row:
                        all_rows.append(row)
                    continue

                # Subdivision/area header like: "ARBOR RIDGE AR-1 AVERAGE $81,600"
                # or "ARBOR RIDGE MEADOWS AR-4 AVERAGE $99,200"
                # Area codes are short alphanumeric with optional hyphen+digit: AR-1, AAS, HEG, BRB3, etc.
                # They appear before "AVERAGE" or "NO CHANGE"
                header_match = re.match(r'^(.+?)\s+([A-Z]{2,5}-?\d*\.?\d*)\s+(?:AVERAGE\s+\$?([\d,]+)|NO\s+CHANGE)', ls)
                if header_match and not ls.startswith("L"):
                    sub_name = header_match.group(1).strip()
                    area_code = header_match.group(2).strip()
                    avg_land = header_match.group(3) or ""
                    # Validate it looks like a real area code (has digit or hyphen, or is short uppercase)
                    if (len(area_code) <= 10 and sub_name.isupper() and
                        not any(kw in sub_name for kw in ["PARCEL", "TOTALS", "$", "SALE", "STD"])):
                        current_sub = sub_name
                        current_area_code = area_code
                        current_avg_land = avg_land.replace(",", "")
                        continue

    fieldnames = ["Subdivision", "Area_Code", "Avg_Land_Value", "Parcel_Number", "Street_Address",
                   "Sale_Date", "Sale_Price", "Terms_of_Sale", "Adj_Sale",
                   "Land_Residual", "Land_Value_2025", "Ratio_LV_SP",
                   "Adj_Land_Value", "Land_Value_2026", "Adj_Alloc_Ratio_LV_SP",
                   "Total_Acres", "ECF_Area", "Land_Table", "Class", "Rate_Group"]

    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Extracted {len(all_rows)} rows to {CSV_PATH}")

    # Write adjustment factors
    adj_path = CSV_PATH.replace(".csv", "_Adjustments.csv")
    if land_adjustments:
        with open(adj_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Area_Code", "Subdivision", "Adjust_Factor"])
            writer.writeheader()
            writer.writerows(land_adjustments)
        print(f"Wrote {len(land_adjustments)} adjustment factors to {adj_path}")

if __name__ == "__main__":
    main()
