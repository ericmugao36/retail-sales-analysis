from openpyxl import load_workbook
from openpyxl.chart import BarChart, LineChart, Reference

file_path = "retail_sales_report.xlsx"

wb = load_workbook(file_path)


# CHART 1: Revenue by Branch
ws = wb["Branch Analysis"]

chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Revenue by Branch"
chart.y_axis.title = "Revenue (KSh)"
chart.x_axis.title = "Branch"

data = Reference(
    ws,
    min_col=2,
    min_row=1,
    max_row=ws.max_row
)

categories = Reference(
    ws,
    min_col=1,
    min_row=2,
    max_row=ws.max_row
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.height = 9
chart.width = 16

ws.add_chart(chart, "G2")


# CHART 2: Revenue by Category
ws = wb["Category Analysis"]

chart = BarChart()
chart.type = "bar"
chart.style = 11
chart.title = "Revenue by Product Category"
chart.x_axis.title = "Revenue (KSh)"
chart.y_axis.title = "Category"

data = Reference(
    ws,
    min_col=2,
    min_row=1,
    max_row=ws.max_row
)

categories = Reference(
    ws,
    min_col=1,
    min_row=2,
    max_row=ws.max_row
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.height = 9
chart.width = 16

ws.add_chart(chart, "G2")


# CHART 3: Monthly Revenue Trend
ws = wb["Monthly Analysis"]

chart = LineChart()
chart.style = 13
chart.title = "Monthly Revenue Trend"
chart.y_axis.title = "Revenue (KSh)"
chart.x_axis.title = "Month"

data = Reference(
    ws,
    min_col=4,
    min_row=1,
    max_row=ws.max_row
)

categories = Reference(
    ws,
    min_col=3,
    min_row=2,
    max_row=ws.max_row
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.height = 9
chart.width = 18

ws.add_chart(chart, "G2")


# Save workbook
wb.save(file_path)

print("Three Excel charts added successfully!")