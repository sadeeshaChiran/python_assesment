import pandas as pd
from tabulate import tabulate

class SalesDataAnalyzer:
    def __init__(self, data):
        self.data = data

    def analyze_monthly_sales(self, month, year):

        print("=" * 80)
        print(f"Monthly Sales Analysis for {month}-{year}")
        print("=" * 80)

        self.data['Date'] = pd.to_datetime(self.data['Date'], format="%m/%d/%Y")

        filtered_data = self.data[
            (self.data['Date'].dt.month == int(month)) & (self.data['Date'].dt.year == int(year))
            ]

        monthly_sales_summary = filtered_data.groupby(['Branch', 'Product line']).agg({
            'Total': 'sum',
            'Quantity': 'count'
        }).reset_index()

        for branch in monthly_sales_summary['Branch'].unique():
            print(f"\nBranch {branch}")

            branch_data = monthly_sales_summary[monthly_sales_summary['Branch'] == branch]

            table_data = []
            for _, row in branch_data.iterrows():
                product_line = row['Product line']
                total_sales = row['Total']
                product_count = row['Quantity']

                table_data.append([product_line, f'Rs.{total_sales:.2f}', product_count])

            headers = ['Product Name', 'Total Income', 'Number of sales']
            print(tabulate(table_data, headers=headers))

    def analyze_price_of_product(self):
        print("=" * 80)
        print("Product Price Analysis")
        print("=" * 80)
        print("\n")

        product_info = {}

        for transaction in self.data.itertuples():
            product_name = transaction._6

            # Update product information
            if product_name not in product_info:
                product_info[product_name] = {'count': 0, 'total_price': 0}

            product_info[product_name]['count'] += 1
            product_info[product_name]['total_price'] += transaction.Total

        table_data = []
        for product, info in product_info.items():
            average_price = info['total_price'] / info['count']
            average_price = f'Rs.{average_price:.2f}'
            total_price_sum = f'Rs.{info["total_price"]:.2f}'
            table_data.append([product, info['count'], total_price_sum, average_price])

        headers = ['Product Name', 'Selling Count', 'Total Income', 'Average Price(One Per Item)']
        print(tabulate(table_data, headers=headers))

    def analyze_weekly_sales(self, week_start_date):
        print("=" * 80)
        print(f"Weekly Sales Analysis for the week starting from {week_start_date}")
        print("=" * 80)
        print("\n")

        branch_info = {}

        week_start = pd.to_datetime(week_start_date)
        week_end = week_start + pd.DateOffset(days=6)

        filtered_data = self.data[
            (self.data['Date'] >= week_start) & (self.data['Date'] <= week_end)
            ]

        table_data = []
        for transaction in filtered_data.itertuples():
            branch_name = transaction.Branch

            if branch_name not in branch_info:
                branch_info[branch_name] = {'count': 0, 'total_sales': 0}

            branch_info[branch_name]['count'] += 1
            branch_info[branch_name]['total_sales'] += transaction.Total

        headers = ['Branch', 'Selling Count', 'Total Income']

        for branch, info in branch_info.items():
            table_data.append([branch, info['count'], f"Rs.{info['total_sales']:.2f}"])

        print(tabulate(table_data, headers=headers))

    def analyze_product_preference(self):
        print("=" * 80)
        print("Product Preference Analysis")
        print("=" * 80)
        print("\n")

        product_totals = {}

        total_sales = 0
        total_count = 0

        for transaction in self.data.itertuples():
            product_name = transaction._6

            if product_name not in product_totals:
                product_totals[product_name] = {'sales': 0, 'count': 0}

            product_totals[product_name]['sales'] += transaction.Total  # Assuming 'Total' is the correct attribute
            product_totals[product_name]['count'] += 1

            total_sales += transaction.Total
            total_count += 1

        for product, totals in product_totals.items():
            totals['percentage'] = (totals['sales'] / total_sales) * 100

        table_data = []
        for product, totals in product_totals.items():
            total_sales_formatted = f'Rs.{totals["sales"]:.2f}'
            table_data.append([product, totals['count'], total_sales_formatted, f"{totals['percentage']:.2f}%"])

        headers = ['Product Name', 'Selling Count', 'Total Income', 'Sales Percentage']
        print(tabulate(table_data, headers=headers))

    def analyze_sales_distribution(self):
        print("=" * 80)
        print("Sales Distribution Analysis")
        print("=" * 80)
        print("\n")

        branch_total_sales = {}

        for transaction in self.data.itertuples():
            branch_name = transaction.Branch

            if branch_name not in branch_total_sales:
                branch_total_sales[branch_name] = 0

            branch_total_sales[branch_name] += transaction.Total

        total_sales_all_branches = sum(branch_total_sales.values())

        distribution_percentage = {branch: total_sales / total_sales_all_branches * 100
                                   for branch, total_sales in branch_total_sales.items()}

        table_data = [[branch, f"{percentage:.2f}%", f'Rs.{branch_total_sales[branch]:.2f}'] for branch, percentage in
                      distribution_percentage.items()]

        headers = ['Branch', 'Sales Distribution', 'Total Income']
        print(tabulate(table_data, headers=headers))


file_path = 'abcde.csv'
data = pd.read_csv(file_path, parse_dates=['Date'])
data['Date'] = pd.to_datetime(data['Date'], format="%m/%d/%Y")

analyzer = SalesDataAnalyzer(data)

print("\n")
analyzer.analyze_monthly_sales("01", "2019")
print("\n")

print("\n")
analyzer.analyze_price_of_product()
print("\n")

print("\n")
analyzer.analyze_weekly_sales("2019-01-01")
print("\n")

print("\n")
analyzer.analyze_product_preference()
print("\n")

print("\n")
analyzer.analyze_sales_distribution()
print("\n")