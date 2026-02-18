#!/usr/bin/env python3
"""Generate Comprehensive Tax Appeal Analysis PDF for University Palisades (UNF) - 3543 Fieldcrest Ln."""
from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "2026_Comprehensive_Tax_Appeal_Analysis.pdf")


class AnalysisPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 5, "Comprehensive Tax Appeal Analysis - University Palisades (UNF)", align="R")
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_heading(self, text, level=1):
        if level == 1:
            self.ln(4)
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(0, 51, 102)
            self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(0, 51, 102)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)
        elif level == 2:
            self.ln(3)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(0, 51, 102)
            self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bold_text(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def italic_text(self, text):
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 10)
        indent = self.l_margin + 5
        self.cell(5, 5.5, "-")
        if bold_prefix:
            self.set_font("Helvetica", "B", 10)
            w = self.get_string_width(bold_prefix) + 1
            self.cell(w, 5.5, bold_prefix)
            self.set_font("Helvetica", "", 10)
            indent += w
        remaining = self.w - self.get_x() - self.r_margin
        if remaining < 20:
            self.ln()
            self.set_x(indent)
        self.multi_cell(0, 5.5, text)

    def numbered_item(self, num, bold_prefix, text):
        self.set_font("Helvetica", "B", 10)
        prefix = f"{num}. {bold_prefix}"
        self.cell(self.get_string_width(prefix) + 2, 5.5, prefix)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def add_table(self, headers, rows, col_widths=None, font_size=8):
        if col_widths is None:
            available = self.w - self.l_margin - self.r_margin
            col_widths = [available / len(headers)] * len(headers)
        self.set_font("Helvetica", "B", font_size)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", font_size)
        for r_idx, row in enumerate(rows):
            fill = r_idx % 2 == 0
            if fill:
                self.set_fill_color(240, 245, 255)
            for i, val in enumerate(row):
                align = "L" if i == 0 else "C"
                self.cell(col_widths[i], 5.5, val, border=1, fill=fill, align=align)
            self.ln()
        self.ln(3)


def main():
    pdf = AnalysisPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title block
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Comprehensive Property Tax", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "Appeal Analysis", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, "University Palisades (UNF), Pittsfield Township", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Based on Township Assessment Data: 2024, 2025, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "Prepared: February 18, 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # Deadline box
    pdf.ln(3)
    pdf.set_fill_color(255, 235, 235)
    pdf.set_draw_color(180, 0, 0)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(180, 0, 0)
    y = pdf.get_y()
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, 10, style="DF")
    pdf.cell(0, 10, "APPEAL DEADLINE: March 10, 2026 at 5:00 PM", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Executive Summary ---
    pdf.section_heading("Executive Summary")
    pdf.body_text(
        "Analysis of three years of Pittsfield Township assessment data (2024-2026) -- including "
        "the Residential Sales Analysis, ECF Analysis, and Land Analysis -- conclusively demonstrates "
        "that the 2026 assessment for 3543 Fieldcrest Ln in the University Palisades subdivision (UNF) "
        "overstates market value. The implied True Cash Value of $506,854 exceeds every single "
        "arm's-length sale ever recorded in the entire subdivision. The township's own ECF data shows "
        "individual Fieldcrest Ln properties with ECFs as low as 0.852, meaning the cost approach "
        "overvalues some homes by nearly 15%."
    )
    pdf.bold_text("For 3543 Fieldcrest Ln specifically:")
    pdf.bullet("2026 SEV: $253,427 -> Implied TCV: $506,854", bold_prefix="")
    pdf.bullet("Assessed Value: $253,427 | Taxable Value: $201,370", bold_prefix="")
    pdf.bullet("Implied TCV is $36,854 above the highest sale ever in University Palisades ($470,000)")
    pdf.bullet("Five Fieldcrest Ln arm's-length comparables average $445,800 (median $440,000)")
    pdf.bullet("Recommended TCV: $430,000-$455,000 (SEV: $215,000-$227,500)")
    pdf.bullet("Potential reduction: $25,927-$38,427 in assessed value")
    pdf.ln(3)

    # --- Section 1: ECF ---
    pdf.section_heading("1. The Township's ECF Data for University Palisades")
    pdf.body_text(
        "The Economic Condition Factor (ECF) is the township's own metric comparing actual arm's-length "
        "sale prices to cost-approach valuations. An ECF below 1.0 means the cost approach overvalues "
        "properties compared to what they actually sell for."
    )

    pdf.section_heading("UNF ECF Trend (3-Year)", level=2)
    pdf.add_table(
        ["Year", "Ave. ECF", "What It Means"],
        [
            ["2024", "N/A", "UNF not included in 2024 ECF summaries"],
            ["2025", "0.974", "Cost values exceed market by 2.6% on average"],
            ["2026", "1.016", "Cost values roughly match market (+1.6%)"],
        ],
        col_widths=[25, 25, 120],
    )

    pdf.section_heading("ECF Per Individual Property (UNF) - 2025", level=2)
    pdf.add_table(
        ["Parcel", "Address", "Sale Price", "Date", "ECF"],
        [
            ["L-12-12-315-027", "3984 Palisades Blvd", "$440,000", "05/23/2023", "0.869"],
            ["L-12-12-315-029", "3960 Palisades Blvd", "$400,000", "08/04/2023", "1.115"],
            ["L-12-12-315-039", "3838 Fieldcrest Ln", "$434,000", "04/20/2022", "1.004"],
            ["L-12-12-320-063", "3745 Fieldcrest Ln", "$470,000", "06/14/2022", "1.252"],
            ["L-12-12-320-067", "3793 Fieldcrest Ln", "$455,000", "06/01/2023", "1.024"],
            ["L-12-12-320-097", "3750 Palisades Blvd", "$446,000", "07/01/2022", "0.915"],
            ["L-12-12-320-101", "3720 Palisades Blvd", "$420,000", "01/17/2023", "0.883"],
            ["L-12-12-320-103", "4542 Palisades Ct", "$420,000", "07/19/2022", "0.876"],
            ["L-12-12-431-149", "3578 Fieldcrest Ln", "$440,000", "08/31/2023", "0.852"],
            ["L-12-12-433-011", "3855 Palisades Blvd", "$376,000", "12/29/2022", "0.835"],
            ["L-12-12-435-079", "3859 Century Ct", "$380,000", "10/05/2022", "1.008"],
            ["L-12-12-435-082", "3899 Century Ct", "$462,500", "02/20/2024", "1.106"],
            ["L-12-12-435-090", "3818 Century Ct", "$420,000", "07/19/2022", "0.920"],
        ],
        col_widths=[32, 32, 22, 22, 18],
        font_size=7,
    )
    pdf.bold_text(
        "8 of 13 properties (62%) have ECFs below 1.0. Fieldcrest Ln ECFs range from 0.852 to 1.252 "
        "-- wide variation even on the same street."
    )

    pdf.section_heading("ECF Per Individual Property (UNF) - 2026", level=2)
    pdf.add_table(
        ["Parcel", "Address", "Sale Price", "Date", "ECF"],
        [
            ["L-12-12-315-027", "3984 Palisades Blvd", "$440,000", "05/23/2023", "0.875"],
            ["L-12-12-315-029", "3960 Palisades Blvd", "$400,000", "08/04/2023", "1.123"],
            ["L-12-12-320-066", "3781 Fieldcrest Ln", "$430,000", "07/23/2024", "1.082"],
            ["L-12-12-320-067", "3793 Fieldcrest Ln", "$455,000", "06/01/2023", "1.033"],
            ["L-12-12-431-149", "3578 Fieldcrest Ln", "$440,000", "08/31/2023", "0.856"],
            ["L-12-12-433-010", "3847 Palisades Blvd", "$454,000", "04/11/2024", "1.112"],
            ["L-12-12-435-082", "3899 Century Ct", "$462,500", "02/20/2024", "1.032"],
        ],
        col_widths=[32, 32, 22, 22, 18],
        font_size=7.5,
    )

    # --- Section 2: Comparable Sales ---
    pdf.section_heading("2. Comparable Sales Analysis")

    pdf.section_heading("Fieldcrest Ln Sales (Most Relevant)", level=2)
    pdf.add_table(
        ["#", "Address", "Sale Price", "Date", "vs $506,854 TCV"],
        [
            ["1", "3781 Fieldcrest Ln", "$430,000", "Jul 23, 2024", "-$76,854 (15.2%)"],
            ["2", "3793 Fieldcrest Ln", "$455,000", "Jun 1, 2023", "-$51,854 (10.2%)"],
            ["3", "3578 Fieldcrest Ln", "$440,000", "Aug 31, 2023", "-$66,854 (13.2%)"],
            ["4", "3838 Fieldcrest Ln", "$434,000", "Apr 20, 2022", "-$72,854 (14.4%)"],
            ["5", "3745 Fieldcrest Ln", "$470,000", "Jun 14, 2022", "-$36,854 (7.3%)"],
            ["6", "3533 Fieldcrest Ln*", "$350,000", "Feb 21, 2025", "-$156,854 (30.9%)"],
        ],
        col_widths=[8, 35, 22, 28, 48],
    )
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 5, "* 3533 Fieldcrest Ln classified as non-arm's-length by township", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.bold_text("Fieldcrest Ln Arm's-Length Statistics (excluding 3533):")
    pdf.bullet("Average: $445,800 (assessment is $61,054 above average)")
    pdf.bullet("Median: $440,000 (assessment is $66,854 above median)")
    pdf.bullet("Range: $430,000-$470,000")
    pdf.bullet("All 5 arm's-length sales are below the implied TCV of $506,854")
    pdf.ln(2)

    pdf.section_heading("All University Palisades Arm's-Length Sales", level=2)
    pdf.add_table(
        ["#", "Address", "Sale Price", "Date"],
        [
            ["1", "3745 Fieldcrest Ln", "$470,000", "Jun 14, 2022"],
            ["2", "3899 Century Ct", "$462,500", "Feb 20, 2024"],
            ["3", "3793 Fieldcrest Ln", "$455,000", "Jun 1, 2023"],
            ["4", "3847 Palisades Blvd", "$454,000", "Apr 11, 2024"],
            ["5", "3750 Palisades Blvd", "$446,000", "Jul 1, 2022"],
            ["6", "3984 Palisades Blvd", "$440,000", "May 23, 2023"],
            ["7", "3578 Fieldcrest Ln", "$440,000", "Aug 31, 2023"],
            ["8", "3838 Fieldcrest Ln", "$434,000", "Apr 20, 2022"],
            ["9", "3781 Fieldcrest Ln", "$430,000", "Jul 23, 2024"],
            ["10", "3972 Palisades Blvd", "$430,000", "May 7, 2024"],
            ["11", "4538 Palisades Ct", "$425,000", "May 18, 2022"],
            ["12", "4542 Palisades Ct", "$420,000", "Jul 19, 2022"],
            ["13", "3720 Palisades Blvd", "$420,000", "Jan 17, 2023"],
            ["14", "3818 Century Ct", "$420,000", "Jul 19, 2022"],
            ["15", "3960 Palisades Blvd", "$400,000", "Aug 4, 2023"],
            ["16", "3979 Lancaster Ct", "$388,000", "Sep 24, 2021"],
            ["17", "3876 Palisades Blvd", "$385,000", "Apr 20, 2021"],
            ["18", "3859 Century Ct", "$380,000", "Oct 5, 2022"],
            ["19", "3855 Palisades Blvd", "$376,000", "Dec 29, 2022"],
            ["20", "3789 Palisades Blvd", "$375,000", "Jun 4, 2021"],
            ["21", "3936 Palisades Blvd", "$315,000", "Sep 2, 2021"],
        ],
        col_widths=[8, 42, 25, 30],
        font_size=7.5,
    )
    pdf.bold_text(
        "No arm's-length sale in University Palisades has ever exceeded $470,000. "
        "The 2026 assessment for 3543 Fieldcrest Ln implies a TCV of $506,854 -- "
        "$36,854 (7.9%) higher than the most expensive home ever sold in the subdivision."
    )
    pdf.body_text(
        "Full subdivision (21 sales): Average $416,452 (over-assessed by $90,402) | "
        "Median $425,000 (over-assessed by $81,854) | Range $315,000-$470,000"
    )

    # --- Section 3: Land Value ---
    pdf.section_heading("3. Land Value Analysis")
    pdf.body_text("The township's land analysis shows how land values in UNF have evolved:")
    pdf.add_table(
        ["Year", "Prior Land Value", "Adjustment Factor", "Current Land Value"],
        [
            ["2024", "$72,500", "1.1594 (+15.9%)", "$84,100"],
            ["2025", "$84,100", "1.0637 (+6.4%)", "$89,500"],
            ["2026", "$89,500", "1.0280 (+2.8%)", "$92,000"],
        ],
        col_widths=[25, 40, 40, 40],
    )
    pdf.bold_text("Total land value increase: 26.9% over 3 years ($72,500 -> $92,000)")
    pdf.body_text(
        "The land adjustment factor has been declining sharply -- from 15.9% in 2024 to just 2.8% in 2026 "
        "-- indicating the assessor recognizes that land value appreciation is slowing significantly."
    )

    pdf.section_heading("Land Residual Analysis", level=2)
    pdf.body_text(
        'The township calculates "land residual" by subtracting building value from sale price. For UNF sales (2026):'
    )
    pdf.add_table(
        ["Address", "Sale Price", "Land Residual", "Ratio LV/SP"],
        [
            ["3984 Palisades Blvd", "$440,000", "$75,229", "0.20"],
            ["3972 Palisades Blvd", "$430,000", "$188,941", "0.21"],
            ["3960 Palisades Blvd", "$400,000", "$147,244", "0.22"],
            ["3781 Fieldcrest Ln", "$430,000", "$140,980", "0.21"],
            ["3793 Fieldcrest Ln", "$455,000", "$130,027", "0.20"],
            ["3578 Fieldcrest Ln", "$440,000", "$68,177", "0.20"],
            ["3847 Palisades Blvd", "$454,000", "$153,895", "0.20"],
            ["3899 Century Ct", "$462,500", "$156,393", "0.19"],
        ],
        col_widths=[40, 28, 30, 25],
    )
    pdf.body_text(
        "The wide variation in land residuals ($68,177 to $188,941) underscores the difficulty of the cost "
        "approach for this subdivision. The assigned land value of $92,000 (2026) represents approximately "
        "20-22% of typical sale prices."
    )

    # --- Section 4: YoY Trend ---
    pdf.section_heading("4. Year-Over-Year Assessment Trend")

    pdf.section_heading("Sales Study Coverage for UNF", level=2)
    pdf.add_table(
        ["Year", "# of UNF Sales in Study", "Sales Date Range"],
        [
            ["2024", "13", "2021-2023 sales"],
            ["2025", "14", "2022-2024 sales"],
            ["2026", "9 (8 arm's + 1 other)", "2023-2025 sales"],
        ],
        col_widths=[25, 55, 65],
    )
    pdf.body_text(
        "The number of sales in the study has been declining -- from 13 in 2024 to 9 in 2026. "
        "Fewer comparable sales means less market evidence supporting the assessments."
    )

    pdf.section_heading("ECF Summary Trend", level=2)
    pdf.add_table(
        ["Year", "UNF in ECF Summary?", "Ave. ECF"],
        [
            ["2024", "No -- not included", "N/A"],
            ["2025", "Yes", "0.974"],
            ["2026", "Yes", "1.016"],
        ],
        col_widths=[25, 55, 40],
    )

    # --- Section 5: Specific Analysis ---
    pdf.section_heading("5. Specific Analysis for 3543 Fieldcrest Ln")

    pdf.section_heading("Your 2026 Assessment", level=2)
    pdf.add_table(
        ["Item", "Value"],
        [
            ["2026 SEV (State Equalized Value)", "$253,427"],
            ["2026 Assessed Value", "$253,427"],
            ["2026 Taxable Value", "$201,370"],
            ["Implied True Cash Value (SEV x 2)", "$506,854"],
        ],
        col_widths=[80, 50],
    )

    pdf.section_heading("Assessment vs. Market Reality", level=2)
    pdf.add_table(
        ["Comparison", "Amount", "Difference"],
        [
            ["Implied TCV", "$506,854", "--"],
            ["Highest sale ever in UNF", "$470,000", "Over by $36,854 (7.9%)"],
            ["Fieldcrest Ln average (5 sales)", "$445,800", "Over by $61,054 (13.7%)"],
            ["Fieldcrest Ln median", "$440,000", "Over by $66,854 (15.2%)"],
            ["Most recent Fieldcrest sale", "$430,000", "Over by $76,854 (17.9%)"],
            ["Full subdivision average", "$416,452", "Over by $90,402 (21.7%)"],
        ],
        col_widths=[52, 28, 52],
        font_size=7.5,
    )
    pdf.bold_text(
        "Your assessment implies a TCV higher than 100% of all arm's-length sales "
        "in the entire University Palisades subdivision."
    )

    pdf.section_heading("Recommended Value", level=2)
    pdf.add_table(
        ["Scenario", "Recommended TCV", "Recommended SEV", "Reduction"],
        [
            ["Conservative (avg)", "$445,800", "$222,900", "$30,527"],
            ["Moderate (median)", "$440,000", "$220,000", "$33,427"],
            ["Market-based (recent)", "$430,000", "$215,000", "$38,427"],
        ],
        col_widths=[38, 38, 38, 28],
    )

    pdf.section_heading("Best Comparables for 3543 Fieldcrest Ln", level=2)
    pdf.add_table(
        ["Rank", "Address", "Sale Price", "Date", "Why Comparable"],
        [
            ["1", "3578 Fieldcrest Ln", "$440,000", "Aug 2023", "Closest address, same section"],
            ["2", "3533 Fieldcrest Ln*", "$350,000", "Feb 2025", "Immediate neighbor (non-arm's)"],
            ["3", "3781 Fieldcrest Ln", "$430,000", "Jul 2024", "Most recent arm's-length"],
            ["4", "3793 Fieldcrest Ln", "$455,000", "Jun 2023", "Same street, arm's-length"],
            ["5", "3838 Fieldcrest Ln", "$434,000", "Apr 2022", "Same street, arm's-length"],
        ],
        col_widths=[12, 32, 22, 22, 55],
        font_size=7.5,
    )
    pdf.italic_text(
        "* The 3533 Fieldcrest Ln sale at $350,000 (Feb 2025) is your immediate neighbor. While classified "
        "as non-arm's-length by the township, if you can demonstrate it was a legitimate market transaction, "
        "it would be powerful evidence of a lower market value."
    )

    # --- Section 6: Legal Framework ---
    pdf.section_heading("6. Legal Framework")
    pdf.section_heading("Key Legal Standards", level=2)
    pdf.add_table(
        ["Principle", "Citation", "Application"],
        [
            ["TCV = usual selling price", "MCL 211.27(1)", "Sales comps are the primary evidence"],
            ["No presumption for assessor", "Alhi v Orion Twp, 110 Mich App 764", "Burden does NOT favor assessor"],
            ["Sales comparison most persuasive", "Meadowlanes v Holland, 437 Mich 473", "For residential, comps trump cost approach"],
            ["Independent duty to find correct value", "Great Lakes v Ecorse, 227 Mich App 379", "Tribunal must independently evaluate"],
            ["Arm's-length transaction standard", "Huron Ridge v Ypsilanti, 275 Mich App 23", "Non-arm's-length sales are excluded"],
        ],
        col_widths=[48, 55, 67],
        font_size=7.5,
    )

    pdf.section_heading("Proposal A Taxable Value", level=2)
    pdf.body_text(
        "Your current taxable value is $201,370, which is already below the SEV of $253,427. "
        "Even if the assessed value is reduced to $222,900 (recommended conservative SEV), "
        "it would still be above the taxable value. However, the reduction still benefits you by:"
    )
    pdf.bullet("Constraining future taxable value growth (TV grows from the lower base)")
    pdf.bullet("Establishing a lower baseline if the property is transferred (TV resets to SEV upon sale)")
    pdf.bullet("Demonstrating a pattern for future appeals")
    pdf.bullet("If the SEV is reduced below the taxable value ($201,370), your taxes decrease immediately")
    pdf.ln(2)

    # --- Section 7: Deadlines ---
    pdf.section_heading("7. Appeal Process & Critical Deadlines")

    pdf.section_heading("Step 1: Board of Review (REQUIRED)", level=2)
    pdf.add_table(
        ["Detail", "Information"],
        [
            ["Deadline", "March 10, 2026 at 5:00 PM"],
            ["Organizational Meeting", "March 3, 2026, 9:00 AM"],
            ["Public Hearings", "Mar 9 (9am-12pm, 6pm-9pm), Mar 10 (9am-12pm), Mar 11 (1pm-5pm)"],
            ["Location", "6201 W. Michigan Ave, Ann Arbor, MI 48108"],
            ["Phone", "734-822-3115"],
            ["Email", "assessing@pittsfield-mi.gov"],
            ["Form", "L-4035 Petition to Board of Review"],
            ["Written petitions", "Accepted in lieu of personal appearance"],
        ],
        col_widths=[45, 125],
    )

    pdf.section_heading("Step 2: Michigan Tax Tribunal", level=2)
    pdf.add_table(
        ["Detail", "Information"],
        [
            ["Deadline", "July 31, 2026"],
            ["Filing Fee", "None if PRE >= 50%"],
            ["Division", "Small Claims"],
            ["Standard", "De novo (independent determination)"],
            ["Burden", "Petitioner, preponderance of evidence"],
            ["File", "michigan.gov/taxtrib"],
        ],
        col_widths=[45, 125],
    )


    # --- Section 8: Action Items ---
    pdf.section_heading("8. Recommended Action Items")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 7, "Before March 10, 2026:", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.numbered_item("1", "Pull your property record card ",
        "from BSA Online (bsaonline.com/?uid=193) using your parcel number. "
        "Verify all physical characteristics (sq ft, beds, baths, lot size, condition) are correct. "
        "Any errors strengthen your case.")
    pdf.ln(1)
    pdf.numbered_item("2", "Your key argument: ",
        "Your implied TCV of $506,854 exceeds every single arm's-length sale in University Palisades. "
        "The five Fieldcrest Ln comparables average $445,800. Request a reduction to an SEV of "
        "$215,000-$222,900 (TCV $430,000-$445,800).")
    pdf.ln(1)
    pdf.numbered_item("3", "Investigate the 3533 Fieldcrest Ln sale ",
        "($350,000, Feb 2025). This is your immediate neighbor. If this was a legitimate market "
        "transaction, it could significantly support your appeal.")
    pdf.ln(1)
    pdf.numbered_item("4", "Request the assessor's sales study ",
        "used to value your specific property (you have this right under Michigan law).")
    pdf.ln(1)
    pdf.numbered_item("5", "Complete Form L-4035 ", "and submit with:")
    pdf.bullet("This comparable sales analysis")
    pdf.bullet("The ECF data from the township's own documents")
    pdf.bullet("Any property-specific issues (needed repairs, functional obsolescence)")
    pdf.bullet("Professional appraisal if available ($300-$500)")
    pdf.ln(1)
    pdf.numbered_item("6", "Submit by March 10, 2026 at 5:00 PM", "")
    pdf.bullet("In person at 6201 W. Michigan Ave, Ann Arbor, MI 48108")
    pdf.bullet("By mail (certified, return receipt): same address")
    pdf.bullet("Or call 734-822-3115 to schedule a hearing appointment")
    pdf.ln(1)
    pdf.numbered_item("7", "If Board of Review denies: ",
        "File with Michigan Tax Tribunal by July 31, 2026")
    pdf.ln(4)

    # --- Data Sources ---
    pdf.section_heading("Data Sources")
    pdf.body_text("All data in this analysis comes from official Pittsfield Township documents:")
    sources = [
        "2024 Residential Sale Analysis (35 pages, 1,263 sales)",
        "2024 Residential ECF Analysis (36 pages, 851 properties)",
        "2024 Residential Land Analysis (31 pages, 1,120 properties)",
        "2025 Sales Study - Residential (34 pages, 972 sales)",
        "2025 Residential ECF Analysis (42 pages, 800 properties)",
        "2025 Residential Land Analysis (36 pages, 912 properties)",
        "2026 Residential Sales Analysis (40 pages, 803 sales)",
        "2026 Residential ECF Analysis (48 pages, 660 properties)",
        "2026 Residential Land Analysis (36 pages, 742 properties)",
    ]
    for s in sources:
        pdf.bullet(s)
    pdf.ln(3)
    pdf.italic_text(
        "These documents are available from the Pittsfield Township Assessing Office "
        "and at pittsfield-mi.gov/2230/Property-Assessment-Data."
    )

    pdf.output(OUTPUT)
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()
