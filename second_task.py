import requests
from bs4 import BeautifulSoup
import csv
import os


def get_table_data():
    url = 'https://bnb.bg/Statistics/StInterbankForexMarket/index.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the specified name
    table = soup.find('table', {'class': 'table'})
    # Check if the table is found
    if table:
        # Extract data_rows from the table
        data_rows = []
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            data_row = [col.get_text(strip=True) for col in columns]
            data_rows.append(data_row)

        return data_rows
    else:
        print("Table not found on the webpage.")
        return None


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)


def compare_and_rewrite_csv(data, filename):
    # Check if the CSV file exists
    if os.path.exists(filename):
        # Read the existing CSV file
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            existing_data = [row for row in csv.reader(csvfile)]

        # Compare data and rewrite only if different
        if data != existing_data:
            save_to_csv(data, filename)
            print("Table has been updated. CSV file rewritten.")
        else:
            print("Table has not changed. CSV file remains the same.")
    else:
        # Save the initial data to CSV
        save_to_csv(data, filename)
        print("Initial table saved to CSV.")


if __name__ == "__main__":
    # Get the latest data from the website
    latest_data = get_table_data()

    if latest_data:
        # Sort the list in descending order by values in column 'обем продадени'
        latest_data.sort(key=lambda x: float(x[6].replace(' ', '').replace(',', '.')) if len(x) > 6 else 0.0, reverse=True)

        # Define the CSV filename
        csv_filename = 'spot_trading_data.csv'

        # Compare and rewrite CSV if necessary
        compare_and_rewrite_csv(latest_data, csv_filename)
