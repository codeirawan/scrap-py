from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Translation dictionary
translations = {
    "Dragon": "Naga",
    "Horse": "Kuda",
    "Tiger": "Macan",
    "Rabbit": "Kelinci",
    "Monkey": "Monyet",
    "Sheep": "Kambing",
    "Snake": "Ular",
    "Dog": "Anjing",
    "Ox": "Kerbau",
    "Pig": "Babi",
    "Rooster": "Ayam",
    "Rat": "Tikus",
    "Metal": "Logam",
    "Wood": "Kayu",
    "Earth": "Tanah",
    "Fire": "Api",
    "Water": "Air"
}

# Function to translate zodiac and elements
def translate(text):
    for key, value in translations.items():
        text = text.replace(key, value)
    return text

# Function to format date
def format_date(year, month, day):
    return f"{year}/{month:02d}/{day:02d}"

# Input date from user
year = input("Enter year (e.g., 2024): ")
month = input("Enter month (e.g., 7 for July): ")
day = input("Enter day (e.g., 8): ")

# Validate and parse input
try:
    year = int(year)
    month = int(month)
    day = int(day)
except ValueError:
    print("Invalid input. Please enter numeric values for year, month, and day.")
    exit()

# URL to fetch the data from
url = f'https://www.prokerala.com/general/calendar/date.php?theme=unity&year={year}&month={month}&day={day}&calendar=chinese&la=&sb=1&loc=1816670'

# Fetch the HTML content from the URL
response = requests.get(url)
html_content = response.text

# Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract relevant data
data = {}

# Extract modal header information
modal_header = soup.find('h4', class_='modal-title')
if modal_header:
    data['Title'] = modal_header.text.strip()

# Extract modal body information
modal_body = soup.find('div', class_='modal-body')
if modal_body:
    tables = modal_body.find_all('table', class_='table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            key_elem = row.find('th')
            value_elem = row.find('td')
            if key_elem and value_elem:
                key = key_elem.text.strip().rstrip(':')
                value = value_elem.text.strip()
                data[key] = value

# Prepare data for saving to a text file
date_format = format_date(year, month, day)
day_piller = translate(data.get('Day Piller', ''))
month_piller = translate(data.get('Month Piller', ''))
year_piller = translate(data.get('Year Piller', ''))
animal = translate(data.get('Animal', ''))
element = translate(data.get('Element', ''))
planet = translate(data.get('Planet', ''))
color = translate(data.get('Color', ''))
fixed_element = translate(data.get('Fixed Element', ''))
yin_yang = translate(data.get('Yin / Yang', ''))

# Define output file path
output_file = 'output.txt'

# Save data to a text file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(f"{date_format}|{day_piller}|{month_piller}|{year_piller}|{animal}|{element}|{planet}|{color}|{fixed_element}|{yin_yang}\n")

print(f"Data saved to {output_file}")
