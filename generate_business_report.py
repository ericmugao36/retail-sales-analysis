import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

# Load cleaned dataset
df = pd.read_csv("retail_sales_clean.csv")
df["sale_date"] = pd.to_datetime(df["sale_date"])

# Calculate key metrics
revenue = df["revenue_ksh"].sum()
profit = df["profit_ksh"].sum()
margin = profit / revenue * 100
transactions = len(df)
units = df["quantity"].sum()

branches = df.groupby("branch")["revenue_ksh"].sum().sort_values(
    ascending=False
)

categories = df.groupby("category").agg(
    Revenue=("revenue_ksh", "sum"),
    Profit=("profit_ksh", "sum")
).sort_values("Revenue", ascending=False)

products = df.groupby("product").agg(
    Revenue=("revenue_ksh", "sum"),
    Units=("quantity", "sum")
).sort_values("Revenue", ascending=False)

monthly = df.groupby(
    df["sale_date"].dt.month
)["revenue_ksh"].sum()

best_month = monthly.idxmax()
worst_month = monthly.idxmin()

month_names = {
    i: pd.Timestamp(2025, i, 1).strftime("%B")
    for i in range(1, 13)
}

# Create PDF
pdf = SimpleDocTemplate(
    "Retail_Sales_Analysis_Report.pdf",
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ReportTitle",
    parent=styles["Title"],
    fontSize=24,
    leading=30,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=12
))

styles.add(ParagraphStyle(
    name="SectionHeading",
    parent=styles["Heading2"],
    fontSize=15,
    textColor=colors.HexColor("#17365D"),
    spaceBefore=14,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name="ReportBody",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15,
    spaceAfter=8
))

story = []

# Cover
story.append(Spacer(1, 3*cm))
story.append(Paragraph(
    "RETAIL SALES ANALYSIS",
    styles["ReportTitle"]
))

story.append(Paragraph(
    "Business Performance Report | 2025",
    styles["Heading2"]
))

story.append(Spacer(1, 1*cm))

story.append(Paragraph(
    "A data-driven assessment of sales, profitability, "
    "branch performance and product categories.",
    styles["ReportBody"]
))

story.append(Spacer(1, 2*cm))

story.append(Paragraph(
    "<b>Prepared by:</b> Yuri Solutions &amp; Products",
    styles["ReportBody"]
))

story.append(Paragraph(
    "<b>Reporting period:</b> January – December 2025",
    styles["ReportBody"]
))

story.append(Paragraph(
    "<b>Data:</b> Simulated retail transaction dataset "
    "created for demonstration purposes.",
    styles["ReportBody"]
))

story.append(PageBreak())

# Executive summary
story.append(Paragraph(
    "1. Executive Summary",
    styles["SectionHeading"]
))

story.append(Paragraph(
    f"The business generated total revenue of "
    f"<b>KSh {revenue:,.2f}</b> and recorded profit of "
    f"<b>KSh {profit:,.2f}</b> during the reporting period. "
    f"This represents a profit margin of <b>{margin:.2f}%</b>. "
    f"The analysis covers {transactions} cleaned transactions "
    f"and {units:,.0f} units sold.",
    styles["ReportBody"]
))

# KPI table
kpi_data = [
    ["Performance Indicator", "Result"],
    ["Total Revenue", f"KSh {revenue:,.2f}"],
    ["Total Profit", f"KSh {profit:,.2f}"],
    ["Profit Margin", f"{margin:.2f}%"],
    ["Transactions", f"{transactions:,}"],
    ["Units Sold", f"{units:,.0f}"]
]

table = Table(kpi_data, colWidths=[8*cm, 7*cm])

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("PADDING", (0, 0), (-1, -1), 8),
    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F5F9"))
]))

story.append(table)

# Branch performance
story.append(Paragraph(
    "2. Branch Performance",
    styles["SectionHeading"]
))

story.append(Paragraph(
    f"The Meru branch recorded the highest revenue at "
    f"<b>KSh {branches.iloc[0]:,.2f}</b>, followed by "
    f"{branches.index[1]} and {branches.index[2]}. "
    "This suggests that branch-level differences deserve "
    "further investigation.",
    styles["ReportBody"]
))

branch_data = [["Branch", "Revenue"]]

for branch, amount in branches.items():
    branch_data.append([branch, f"KSh {amount:,.2f}"])

table = Table(branch_data, colWidths=[8*cm, 7*cm])

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("PADDING", (0, 0), (-1, -1), 7)
]))

story.append(table)

# Category analysis
story.append(Paragraph(
    "3. Product Category Performance",
    styles["SectionHeading"]
))

story.append(Paragraph(
    f"{categories.index[0]} was the leading category, "
    f"generating KSh {categories.iloc[0]['Revenue']:,.2f} "
    "in revenue. However, groceries recorded a comparatively "
    "low profit margin, indicating that costs and pricing "
    "may require attention.",
    styles["ReportBody"]
))

category_data = [["Category", "Revenue", "Profit"]]

for category, row in categories.iterrows():
    category_data.append([
        category,
        f"KSh {row['Revenue']:,.2f}",
        f"KSh {row['Profit']:,.2f}"
    ])

table = Table(
    category_data,
    colWidths=[5*cm, 5*cm, 5*cm]
)

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("FONTSIZE", (0, 0), (-1, -1), 8)
]))

story.append(table)

# Top products
story.append(Paragraph(
    "4. Leading Products",
    styles["SectionHeading"]
))

story.append(Paragraph(
    "The following five products generated the highest revenue:",
    styles["ReportBody"]
))

product_data = [["Product", "Revenue", "Units Sold"]]

for product, row in products.head(5).iterrows():
    product_data.append([
        product,
        f"KSh {row['Revenue']:,.2f}",
        f"{row['Units']:,.0f}"
    ])

table = Table(
    product_data,
    colWidths=[6*cm, 5*cm, 4*cm]
)

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("FONTSIZE", (0, 0), (-1, -1), 8)
]))

story.append(table)

# Monthly performance
story.append(Paragraph(
    "5. Monthly Sales Performance",
    styles["SectionHeading"]
))

story.append(Paragraph(
    f"{month_names[best_month]} was the strongest month, "
    f"with revenue of KSh {monthly.loc[best_month]:,.2f}. "
    f"{month_names[worst_month]} recorded the lowest revenue "
    f"at KSh {monthly.loc[worst_month]:,.2f}. "
    "The business should investigate seasonal demand, "
    "promotional activity and stock availability.",
    styles["ReportBody"]
))

# Recommendations
story.append(Paragraph(
    "6. Business Recommendations",
    styles["SectionHeading"]
))

recommendations = [
    "<b>Study the Meru branch:</b> Identify the sales practices, "
    "customer demand and product mix contributing to its strong performance.",

    "<b>Review grocery profitability:</b> Examine supplier prices, "
    "discounts and selling prices to understand the low margin.",

    "<b>Protect leading products:</b> Monitor stock levels for "
    "high-revenue products, particularly cooking pots and women's dresses.",

    "<b>Investigate monthly fluctuations:</b> Examine why February "
    "performed strongly while April was comparatively weak.",

    "<b>Monitor profitability:</b> Track profit margins alongside "
    "revenue when making pricing and expansion decisions."
]

for recommendation in recommendations:
    story.append(Paragraph(
        "• " + recommendation,
        styles["ReportBody"]
    ))

# Conclusion
story.append(Paragraph(
    "7. Conclusion",
    styles["SectionHeading"]
))

story.append(Paragraph(
    "The analysis indicates that the business is profitable overall, "
    "but performance varies across branches and product categories. "
    "Management can use these findings to improve pricing decisions, "
    "inventory planning and branch-level performance monitoring.",
    styles["ReportBody"]
))

story.append(Spacer(1, 1*cm))

story.append(Paragraph(
    "<i>Report prepared by Yuri Solutions &amp; Products. "
    "All figures are based on a simulated dataset and are intended "
    "for analytical demonstration.</i>",
    styles["Italic"]
))


# Page numbering
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(
        A4[0] / 2,
        1*cm,
        f"Yuri Solutions & Products | Page {doc.page}"
    )
    canvas.restoreState()


pdf.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
)

print("Business report created successfully!")
print("File: Retail_Sales_Analysis_Report.pdf")