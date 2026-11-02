from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

file_path = "retail_sales_report.xlsx"

wb = load_workbook(file_path)

# Professional colours
header_fill = PatternFill(
    fill_type="solid",
    fgColor="17365D"
)

header_font = Font(
    color="FFFFFF",
    bold=True,
    size=11
)

currency_format = '"KSh "#,##0.00'
number_format = '#,##0'
percentage_format = '0.00"%"'

for ws in wb.worksheets:

    # Format headers
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Freeze header row
    ws.freeze_panes = "A2"

    # Add filters
    ws.auto_filter.ref = ws.dimensions

    # Adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(
            column[0].column
        )

        for cell in column:
            if cell.value is not None:
                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        ws.column_dimensions[column_letter].width = min(
            max_length + 4,
            35
        )

# Format currency columns
currency_columns = {
    "Cleaned Data": [
        "unit_price_ksh",
        "unit_cost_ksh",
        "gross_sales_ksh",
        "discount_ksh",
        "revenue_ksh",
        "total_cost_ksh",
        "profit_ksh"
    ],
    "Branch Analysis": ["Revenue", "Profit"],
    "Category Analysis": ["Revenue", "Profit"],
    "Monthly Analysis": ["Revenue", "Profit"]
}

for sheet_name, columns in currency_columns.items():
    ws = wb[sheet_name]

    for column in columns:
        column_index = None

        for cell in ws[1]:
            if cell.value == column:
                column_index = cell.column
                break

        if column_index:
            for row in range(2, ws.max_row + 1):
                ws.cell(
                    row=row,
                    column=column_index
                ).number_format = currency_format

# Format summary values
ws = wb["Sales Summary"]

for row in range(2, ws.max_row + 1):
    metric = ws.cell(row=row, column=1).value
    value_cell = ws.cell(row=row, column=2)

    if "KSh" in metric:
        value_cell.number_format = currency_format

    elif "Margin" in metric:
        value_cell.number_format = percentage_format

    else:
        value_cell.number_format = number_format

# Add Excel tables to data sheets
for sheet_name in [
    "Cleaned Data",
    "Branch Analysis",
    "Category Analysis",
    "Monthly Analysis"
]:
    ws = wb[sheet_name]

    table = Table(
        displayName=sheet_name.replace(" ", "") + "Table",
        ref=ws.dimensions
    )

    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )

    table.tableStyleInfo = style
    ws.add_table(table)

# Save formatted workbook
wb.save(file_path)

print("Excel workbook professionally formatted!")