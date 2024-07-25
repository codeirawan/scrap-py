from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

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

# Function to fetch and save data for a range of dates
def fetch_and_save_data(start_date, end_date, output_file):
    current_date = start_date
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Tanggal dalam format yyyy/mm/dd|Day Piller|Month Piller|Year Piller|Animal|Element|Planet|Color|Fixed Element|Yin Yang\n")
        while current_date <= end_date:
            year, month, day = current_date.year, current_date.month, current_date.day
            date_format = format_date(year, month, day)
            url = f'https://www.prokerala.com/general/calendar/date.php?theme=unity&year={year}&month={month}&day={day}&calendar=chinese&la=&sb=1&loc=1816670'
            
            try:
                # Fetch the HTML content from the URL
                response = requests.get(url)
                response.raise_for_status()  # Raise exception for bad response status
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
                day_piller = translate(data.get('Day Piller', ''))
                month_piller = translate(data.get('Month Piller', ''))
                year_piller = translate(data.get('Year Piller', ''))
                animal = translate(data.get('Animal', ''))
                element = translate(data.get('Element', ''))
                planet = translate(data.get('Planet', ''))
                color = translate(data.get('Color', ''))
                fixed_element = translate(data.get('Fixed Element', ''))
                yin_yang = translate(data.get('Yin / Yang', ''))
                
                # Write data to file
                file.write(f"{date_format}|{day_piller}|{month_piller}|{year_piller}|{animal}|{element}|{planet}|{color}|{fixed_element}|{yin_yang}\n")
            
            except requests.RequestException as e:
                print(f"Error fetching data for {date_format}: {e}")
            
            # Move to the next date
            current_date += timedelta(days=1)
    
    print(f"Data saved to {output_file}")

# Function to get valid date input from user
def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date
        except ValueError:
            print("Invalid date format. Please enter date in yyyy-mm-dd format.")

# Main function to control program flow
def main():
    print("Enter the date range (format: yyyy-mm-dd)")
    start_date = get_date_input("Enter start date: ")
    end_date = get_date_input("Enter end date: ")
    output_file = 'output_range.txt'
    
    fetch_and_save_data(start_date, end_date, output_file)

if __name__ == "__main__":
    main()
