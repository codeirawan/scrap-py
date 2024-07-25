import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def scrape_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Request Status Code: {response.status_code}")  # Print status code for debugging
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get search results (adjust according to the actual HTML structure from Google)
    search_results = soup.find_all("div", class_="g")  # Adjust to the correct class or attribute
    
    print(f"Number of search results found: {len(search_results)}")  # Print number of search results found for debugging
    
    scraped_data = []
    
    # Process and analyze results according to Google's HTML structure
    for result in search_results:
        try:
            title = result.find("h3").get_text()  # Example: get text from <h3> tag for title
            link = result.find("a")["href"]  # Example: get href attribute from <a> tag for link
            
            # Additional: try to find phone number
            phone_number = None
            text = result.get_text()  # Get all text from the result
            
            # Example regex to find phone number pattern (adjust based on actual pattern)
            phone_regex = r"\b(?:\+\d{1,2}\s?)?\(?(?:\d{2,3})?\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b"
            match = re.search(phone_regex, text)
            
            if match:
                phone_number = match.group(0)
                
                # Check if the extracted number is within the range of 9 to 13 digits
                digits_only = re.sub(r'\D', '', phone_number)  # Remove non-digit characters
                if 9 <= len(digits_only) <= 13:
                    phone_number = digits_only
                else:
                    phone_number = None
            
            # Additional check for WhatsApp in title or link
            if 'wa ' in title.lower() or 'wa ' in link.lower() or 'wa.me' in link or 'api.whatsapp.com' in link:
                # Extract the phone number from the URL
                phone_number_from_link = re.search(r'wa\s?(\d{9,13})', title, re.IGNORECASE)  # Search for 'wa' followed by digits in title
                if not phone_number_from_link:
                    phone_number_from_link = re.search(r'wa\s?(\d{9,13})', link, re.IGNORECASE)  # Search for 'wa' followed by digits in link
                if phone_number_from_link:
                    phone_number = phone_number_from_link.group(1)
            
            # Handle Carousell specific extraction
            if 'carousell.com' in link:
                carousell_response = requests.get(link, headers=headers)
                carousell_soup = BeautifulSoup(carousell_response.text, 'html.parser')
                
                # Find description text which often contains WhatsApp number
                description = carousell_soup.find('meta', property='og:description')['content']
                
                # Try to find WhatsApp number from description
                phone_number_from_desc = re.search(r'wa\s?(\d{9,13})', description, re.IGNORECASE)
                if phone_number_from_desc:
                    phone_number = phone_number_from_desc.group(1)
            
            scraped_data.append({"Title": title, "Link": link, "Phone Number": phone_number})
        
        except Exception as e:
            print(f"Error processing result: {e}")
    
    return scraped_data

def save_to_excel(data, filename="scraped_data.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename} successfully.")

if __name__ == "__main__":
    query = "catering area jakarta harga 10-15rb"
    results = scrape_google(query)
    
    if results:
        print(f"Number of results retrieved: {len(results)}")
        print(results)
        
        save_to_excel(results)
    else:
        print("No results retrieved.")
