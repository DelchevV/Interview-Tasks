import requests
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'
response = requests.get(url)

# Read the HTML table directly into a DataFrame
tables = pd.read_html(response.text)

# Find the correct table based on headers or other criteria
for table in tables:
    if 'Country' in table.columns and 'Official figure' in table.columns:
        countries_df = table[['Country', 'Official figure']]
        break
else:
    print("Table not found. Please check if the Wikipedia page structure has changed.")
    exit()

# Convert 'Official figure' column to numeric, filling NaN values with 0
countries_df['Official figure'] = pd.to_numeric(countries_df['Official figure'], errors='coerce').fillna(0).astype(int)

# Create countries_dictionary
countries_dictionary = {}
for index, row in countries_df.iterrows():
    country = row['Country']
    if country == 'European Union':
        continue

    population = int(row['Official figure'])
    countries_dictionary[country] = {'country_population': population}

# Calculate total_country_population
total_country_population = sum(country_data['country_population'] for country_data in countries_dictionary.values())

# Calculate and add country_population_percentage to the dictionary
for country, country_data in countries_dictionary.items():
    percentage = (country_data['country_population'] / total_country_population) * 100
    country_data['country_population_percentage'] = round(percentage, 1)

# Print the results
print("Total Country Population:", total_country_population)
print(countries_dictionary)
