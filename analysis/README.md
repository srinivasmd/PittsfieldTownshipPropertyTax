# Analysis - Pittsfield Township Assessment Data

Three years of Pittsfield Township residential assessment data (2024-2026) converted from PDF to CSV, covering **all residential areas** in the township.

## Folders

| Folder | Contents |
|--------|----------|
| `2024/` | 2024 source PDFs, conversion scripts, and CSVs (1,263 sales, 851 ECF, 1,120 land) |
| `2025/` | 2025 source PDFs, conversion scripts, and CSVs (972 sales, 800 ECF, 912 land) |
| `2026/` | 2026 source PDFs, conversion scripts, and CSVs (803 sales, 660 ECF, 742 land) |
| `PaulinaDrAnalysis/` | Analysis and appeal template specific to Meadows of Arbor Ridge (AR-4) |

## How to Use for Your Area

1. Find your **ECF area code** (e.g., AR-1, AV-1, WW-3) on your assessment notice or at BSA Online (bsaonline.com/?uid=193)
2. Filter the CSVs by your area code to find:
   - **ECF summaries CSV:** Your area's average ECF (below 1.0 = cost approach overvalues)
   - **Sales CSV:** Comparable arm's-length sales in your area
   - **Land CSV:** Land value trends and adjustment factors for your area
3. Use the Paulina Dr Word template as a starting point for your appeal -- replace the AR-4 data with your own area's numbers

## CSV Column Reference

### Sales Analysis CSV
`Parcel_Number, Street_Address, Sale_Date, Sale_Price, Instrument, Terms_of_Sale, Adj_Sale, Asd_When_Sold, Ratio, Cur_Appraisal, ECF_Area, Land_Table, Class, Rate_Group`

### ECF Analysis CSV
`Subdivision, ECF_Area_Code, Parcel_Number, Street_Address, Sale_Date, Sale_Price, Adj_Sale, Land_Value, Land_Yard, Bldg_Residual, Cost_Man, ECF, Building_Style`

### ECF Summaries CSV
`ECF_Area, Subdivision, Ave_ECF`

### Land Analysis CSV
`Subdivision, Area_Code, Avg_Land_Value, Parcel_Number, Street_Address, Sale_Date, Sale_Price, Terms_of_Sale, Adj_Sale, Land_Residual, Land_Value_{prior_year}, Ratio_LV_SP, Adj_Land_Value, Land_Value_{current_year}, Adj_Alloc_Ratio_LV_SP, Total_Acres, ECF_Area, Land_Table, Class, Rate_Group`

### Land Adjustments CSV
`Area_Code, Subdivision, Adjust_Factor`
