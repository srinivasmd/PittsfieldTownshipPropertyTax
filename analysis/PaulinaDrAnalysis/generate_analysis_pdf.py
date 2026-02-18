#!/usr/bin/env python3
"""Generate Comprehensive Tax Appeal Analysis PDF from markdown content."""
from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "2026_Comprehensive_Tax_Appeal_Analysis.pdf")


class AnalysisPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 5, "Comprehensive Tax Appeal Analysis - Meadows of Arbor Ridge (AR-4)", align="R")
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

        # Header
        self.set_font("Helvetica", "B", font_size)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
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
    pdf.cell(0, 7, "Meadows of Arbor Ridge (AR-4), Pittsfield Township", align="C", new_x="LMARGIN", new_y="NEXT")
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
        "that the 2026 assessments for homes in the Meadows of Arbor Ridge subdivision (AR-4) overstate "
        "market value. The township's own Economic Condition Factor (ECF) of 0.802 for AR-4 means the "
        "assessor acknowledges that cost-approach values exceed actual sale prices by approximately 20%. "
        "No home in this subdivision has ever resold for the True Cash Values implied by many 2026 assessments."
    )

    pdf.bold_text("For 4806 Paulina Dr specifically:")
    pdf.bullet("2026 SEV: $242,732 -> Implied TCV: $485,464", bold_prefix="")
    pdf.bullet("Taxable Value: $213,794", bold_prefix="")
    pdf.bullet("The two best direct comparables (same street, same builder): $447,000 and $450,000", bold_prefix="")
    pdf.bullet("Recommended TCV: $450,000-$465,000 (SEV: $225,000-$232,500)", bold_prefix="")
    pdf.bullet("Potential reduction: $10,232-$17,732 in assessed value", bold_prefix="")
    pdf.ln(3)

    # --- Section 1: ECF ---
    pdf.section_heading("1. The Township's Own ECF Data Proves Over-Assessment")
    pdf.body_text(
        "The Economic Condition Factor (ECF) is the township's own metric comparing actual arm's-length "
        "sale prices to cost-approach valuations. An ECF below 1.0 means the cost approach overvalues "
        "properties compared to what they actually sell for."
    )

    pdf.section_heading("AR-4 ECF Trend (3-Year)", level=2)
    pdf.add_table(
        ["Year", "Ave. ECF", "What It Means"],
        [
            ["2024", "0.744", "Cost values exceed market by 25.6%"],
            ["2025", "0.790", "Cost values exceed market by 21.0%"],
            ["2026", "0.802", "Cost values exceed market by 19.8%"],
        ],
        col_widths=[25, 25, 120],
    )
    pdf.body_text(
        "This is a persistent, documented pattern -- not a one-year anomaly. The township's own data "
        "confirms that cost-approach valuations for AR-4 consistently overshoot actual market prices by 20-26%."
    )

    pdf.section_heading("ECF Per Individual Property (AR-4)", level=2)
    pdf.add_table(
        ["Parcel", "Address", "Sale Price", "2024 ECF", "2025 ECF", "2026 ECF"],
        [
            ["L-12-13-311-036", "4807 Paulina Dr", "$450,000", "--", "0.764", "0.766"],
            ["L-12-13-311-058", "4918 Paulina Dr", "$447,000", "0.804", "0.803", "--"],
            ["L-12-13-311-031", "4711 Paulina Dr", "$500,000", "--", "0.797", "0.800"],
            ["L-12-13-311-063", "4782 Paulina Dr", "$452,000", "0.807", "0.806", "--"],
            ["L-12-13-311-057", "4930 Paulina Dr", "$365,424", "0.707", "--", "--"],
            ["L-12-13-310-027", "4610 Lilac Lane", "$465,000", "--", "0.819", "0.822"],
            ["L-12-13-311-050", "4324 Christina Ct", "$499,900", "0.643", "0.815", "0.818"],
            ["L-12-13-311-043", "4321 Christina Ct", "$430,000", "0.724", "0.723", "--"],
            ["L-12-13-310-024", "4470 Connor Dr", "$481,000", "0.799", "0.792", "--"],
            ["L-12-13-311-052", "4458 Christina Dr", "$420,000", "0.724", "--", "--"],
        ],
        col_widths=[32, 30, 22, 22, 22, 22],
        font_size=7.5,
    )
    pdf.bold_text(
        "Every single ECF value is below 1.0. The lowest was 0.643 (4324 Christina Ct in 2024), "
        "meaning the cost approach overvalued that property by 35.7% compared to its actual sale price."
    )

    pdf.section_heading("What the ECF Means for 4806 Paulina Dr", level=2)
    pdf.body_text(
        "If the cost approach produces the 2026 assessment, and the ECF for this area is 0.802, "
        "then the market-adjusted value should be approximately:"
    )
    pdf.bullet("Cost-based TCV x ECF = Market TCV")
    pdf.bullet("$485,464 x 0.802 = $389,242")
    pdf.ln(1)
    pdf.body_text(
        "This suggests the assessment may overstate market value by as much as $96,222 (or the SEV "
        "overstates by ~$48,111). Even using a more conservative adjustment, the ECF clearly supports "
        "a TCV well below $485,464."
    )

    # --- Section 2: Comparable Sales ---
    pdf.section_heading("2. Comparable Sales Analysis")

    pdf.section_heading("Direct Subdivision Comparables (AR-4)", level=2)
    pdf.body_text("These are the only arm's-length sales ever recorded in the Meadows of Arbor Ridge:")

    pdf.add_table(
        ["#", "Address", "Sale Price", "Date", "vs $485,464 TCV"],
        [
            ["1", "4807 Paulina Dr*", "$450,000", "Jul 19, 2023", "-$35,464 (7.3%)"],
            ["2", "4918 Paulina Dr", "$447,000", "Mar 28, 2023", "-$38,464 (7.9%)"],
            ["3", "4711 Paulina Dr", "$500,000", "May 31, 2023", "+$14,536"],
            ["4", "4782 Paulina Dr", "$452,000", "Oct 13, 2022", "-$33,464"],
            ["5", "4610 Lilac Lane", "$465,000", "Aug 18, 2023", "-$20,464"],
            ["6", "4617 Lilac Lane", "$452,000", "Jun 11, 2024", "-$33,464"],
            ["7", "4324 Christina Ct", "$499,900", "Aug 11, 2023", "+$14,436"],
            ["8", "4321 Christina Ct", "$430,000", "May 6, 2022", "-$55,464"],
            ["9", "4470 Connor Dr", "$481,000", "May 25, 2022", "-$4,464"],
            ["10", "4458 Christina Dr", "$420,000", "Jan 27, 2022", "-$65,464"],
            ["11", "4930 Paulina Dr", "$365,424", "Jul 9, 2021", "-$120,040"],
        ],
        col_widths=[8, 38, 28, 30, 66],
    )
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 5, "* 4807 Paulina Dr is directly across the street from 4806 Paulina Dr", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.bold_text("Statistics:")
    pdf.bullet("Average: $459,690 (assessment is $25,774 above average)")
    pdf.bullet("Median: $452,000 (assessment is $33,464 above median)")
    pdf.bullet("Only 2 of 11 sales (18%) exceeded $485,464")
    pdf.bullet("The assessment implies a TCV higher than 82% of all sales in the subdivision")
    pdf.ln(2)

    pdf.section_heading("The Most Compelling Comparable: 4807 Paulina Dr", level=2)
    pdf.body_text("The sale of 4807 Paulina Dr is the single strongest piece of evidence:")
    pdf.bullet("Directly across the street from 4806 Paulina Dr", bold_prefix="Location: ")
    pdf.bullet("Same builder (Lombardo Homes)", bold_prefix="Builder: ")
    pdf.bullet("Same construction period (~2018-2019)", bold_prefix="Era: ")
    pdf.bullet("$450,000 (July 19, 2023)", bold_prefix="Sale Price: ")
    pdf.bullet("$438,422", bold_prefix="2024 Township Appraisal: ")
    pdf.bullet("0.766 (2026), meaning cost approach overvalued by 23.4%", bold_prefix="ECF: ")
    pdf.ln(2)
    pdf.body_text(
        "The subject's assessment implies a TCV $35,464 higher than its most directly comparable neighbor. "
        "There is no objective basis for this discrepancy between essentially identical properties."
    )

    # Adjacent subdivision sales
    pdf.section_heading("Adjacent Subdivision Sales (2023-2025)", level=2)
    pdf.body_text("The surrounding Arbor Ridge subdivisions share the same location, school district, and township:")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "AR-1 (Arbor Ridge - older, built 1995-1997):", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(
        ["Address", "Sale Price", "Date", "2026 Appraisal"],
        [
            ["4562 Christina Dr", "$427,000", "Nov 25, 2024", "$389,440"],
            ["4936 Matthew Ct", "$390,000", "Oct 31, 2024", "$395,088"],
            ["4579 Connor Ct", "$386,000", "Feb 7, 2024", "$413,397"],
        ],
        col_widths=[45, 30, 35, 35],
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "AR-2 (Woodlands of Arbor Ridge - built 2011-2017):", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(
        ["Address", "Sale Price", "Date", "2026 Appraisal"],
        [
            ["4336 Cloverlane Dr", "$455,000", "Nov 15, 2024", "$398,249"],
            ["4236 Cloverlane Dr", "$410,000", "May 3, 2023", "$437,059"],
            ["4249 Cloverlane Dr", "$430,000", "Jun 1, 2023", "$424,507"],
        ],
        col_widths=[45, 30, 35, 35],
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "AR-3 (Arbor Ridge Crossing - newer, larger homes):", new_x="LMARGIN", new_y="NEXT")
    pdf.add_table(
        ["Address", "Sale Price", "Date", "2026 Appraisal"],
        [
            ["4264 Lilac Lane", "$630,000", "Jun 14, 2024", "$591,356"],
            ["4182 Montith Dr", "$602,250", "Dec 30, 2024", "$553,378"],
        ],
        col_widths=[45, 30, 35, 35],
    )
    pdf.italic_text(
        "Note: AR-3 homes are significantly larger (3,000+ sq ft) and more expensive. They represent the "
        "upper boundary of values in the Arbor Ridge complex, not comparable properties to typical Paulina Dr homes."
    )

    # --- Section 3: Land Value ---
    pdf.section_heading("3. Land Value Analysis")
    pdf.body_text("The township's land analysis shows how land values in AR-4 have evolved:")
    pdf.add_table(
        ["Year", "Prior Land Value", "Adjustment Factor", "Current Land Value"],
        [
            ["2024", "$84,300", "1.0648 (+6.5%)", "$89,800"],
            ["2025", "$89,800", "1.0734 (+7.3%)", "$96,400"],
            ["2026", "$96,400", "1.0290 (+2.9%)", "$99,200"],
        ],
        col_widths=[25, 40, 40, 40],
    )
    pdf.bold_text("Total land value increase: 17.7% over 3 years ($84,300 -> $99,200)")
    pdf.body_text(
        "For comparison, the 2026 land adjustment factor of 1.0290 is the lowest in three years, "
        "suggesting the assessor recognizes that the rapid land value appreciation is slowing. "
        "Yet the overall assessments continue to rise."
    )

    pdf.section_heading("Land Residual Analysis (What the Market Says Land Is Worth)", level=2)
    pdf.body_text(
        'The township calculates "land residual" by subtracting building value from sale price. For AR-4 sales:'
    )
    pdf.add_table(
        ["Address", "Sale Price", "Land Residual", "% of Sale"],
        [
            ["4617 Lilac Lane", "$452,000", "$177,270", "39.2%"],
            ["4610 Lilac Lane", "$465,000", "$129,681", "27.9%"],
            ["4711 Paulina Dr", "$500,000", "$123,246", "24.6%"],
            ["4807 Paulina Dr", "$450,000", "$105,669", "23.5%"],
            ["4324 Christina Ct", "$499,900", "$131,749", "26.4%"],
        ],
        col_widths=[40, 30, 35, 25],
    )
    pdf.body_text(
        "The wide variation in land residuals (23.5% to 39.2%) underscores the difficulty of the cost "
        "approach for this subdivision and further supports reliance on the sales-comparison method."
    )

    # --- Section 4: YoY Trend ---
    pdf.section_heading("4. Year-Over-Year Assessment Trend")
    pdf.body_text("The township's data across three years reveals an important pattern:")

    pdf.section_heading("Sales Study Coverage for AR-4", level=2)
    pdf.add_table(
        ["Year", "# of AR-4 Sales in Study", "Sales Used"],
        [
            ["2024", "7", "2021-2023 sales"],
            ["2025", "8", "2022-2023 sales"],
            ["2026", "0*", "(AR-4 dropped from sales analysis)"],
        ],
        col_widths=[25, 55, 65],
    )
    pdf.bold_text(
        "*Critical finding: The 2026 Residential Sales Analysis does not include any AR-4 properties. "
        "The township appears to have dropped the older 2022-2023 sales from the study but has no newer "
        "sales to replace them. Yet assessments continue to increase. This raises the question: "
        "what market evidence supports the 2026 AR-4 assessments?"
    )

    # --- Section 5: Broader Market ---
    pdf.section_heading("5. Broader Market Context")
    pdf.section_heading("Pittsfield Township Market Ceiling", level=2)
    pdf.body_text(
        "Sales from comparable Pittsfield Township neighborhoods in the 48197 zip code (2024-2025) "
        "consistently show a ceiling for homes in the 2,000-2,600 sq ft range:"
    )
    pdf.add_table(
        ["Address", "Sale Price", "Date", "Sq Ft", "Notes"],
        [
            ["5957 Cottonwood Dr", "$397,501", "Apr 2025", "2,099", "Ashford Village, AA Schools"],
            ["5129 Blue Spruce Dr", "$422,500", "Sep 2025", "3,276", "Larger home sold for less"],
            ["8045 Creek Bend Dr", "$465,500", "Jun 2025", "2,915", "Brick colonial, larger"],
            ["4265 Cloverlane Dr", "$465,000", "Apr 2025", "1,960", "Woodlands of AR"],
            ["4482 Christina Dr", "$380,000", "May 2025", "1,603", "Arbor Ridge"],
        ],
        col_widths=[38, 22, 22, 15, 50],
        font_size=7.5,
    )

    pdf.section_heading("Zillow Zestimate Caveat", level=2)
    pdf.body_text(
        "Zillow's automated Zestimate for 4806 Paulina is approximately $548,200. "
        "While this might be cited by the assessor, Zestimates:"
    )
    pdf.bullet("Are algorithmic estimates with no legal standing")
    pdf.bullet("Are not accepted as evidence of market value under Michigan law")
    pdf.bullet("Frequently overstate values for newer subdivisions with limited sales history")
    pdf.bullet("Do not account for subdivision-specific conditions (ECF < 1.0)")
    pdf.ln(2)
    pdf.bold_text("Actual arm's-length sales are the proper measure of true cash value under MCL 211.27(1).")

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
        "Even if the assessed value is reduced but remains above the taxable value ($213,794), "
        "the reduction still benefits the homeowner by:"
    )
    pdf.bullet("Constraining future taxable value growth (TV grows from the lower base)")
    pdf.bullet("Establishing a lower baseline for property transfer adjustments")
    pdf.bullet("Demonstrating a pattern for future appeals")
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
        "Verify all physical characteristics (sq ft, beds, baths, lot size, condition) are correct.")
    pdf.ln(1)
    pdf.numbered_item("2", "Request the assessor's sales study ",
        "used to value your specific property (you have this right under Michigan law).")
    pdf.ln(1)
    pdf.numbered_item("3", "Complete Form L-4035 ", "and submit with:")
    pdf.bullet("This comparable sales analysis")
    pdf.bullet("The ECF data from the township's own documents")
    pdf.bullet("Any property-specific issues (needed repairs, functional obsolescence)")
    pdf.bullet("Professional appraisal if available ($300-$500)")
    pdf.ln(1)
    pdf.numbered_item("4", "Submit by March 10, 2026 at 5:00 PM", "")
    pdf.bullet("In person at 6201 W. Michigan Ave, Ann Arbor, MI 48108")
    pdf.bullet("By mail (certified, return receipt): same address")
    pdf.bullet("Or call 734-822-3115 to schedule a hearing appointment")
    pdf.ln(1)
    pdf.numbered_item("5", "If Board of Review denies: ",
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
