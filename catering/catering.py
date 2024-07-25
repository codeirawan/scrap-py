from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import openpyxl
import re

def fetch_google_results(query):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration

    # Use the path to your updated chromedriver
    service = Service('D:\\code\\scrap\\chromedriver-win32\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.google.com')

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    results = []

    try:
        # Wait for search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )

        # Find all search result containers
        search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

        for result in search_results:
            try:
                title_element = result.find_element(By.CSS_SELECTOR, 'h3')
                url_element = result.find_element(By.CSS_SELECTOR, 'a')

                title = title_element.text
                url = url_element.get_attribute('href')

                # Check for WhatsApp numbers if available in title or URL
                wa_number = 'N/A'
                wa_match = re.search(r'\+?(\d{1,3}[-.\s]?)?\(?\d{1,4}\)?([-.\s]?\d{1,9}){1,4}', title)
                if not wa_match:
                    wa_match = re.search(r'\+?(\d{1,3}[-.\s]?)?\(?\d{1,4}\)?([-.\s]?\d{1,9}){1,4}', url)

                # Check description for WhatsApp numbers
                description = ""
                description_element = result.find_element(By.CSS_SELECTOR, 'span')
                if description_element:
                    description = description_element.text
                    if not wa_match:
                        wa_match = re.search(r'\+?(\d{1,3}[-.\s]?)?\(?\d{1,4}\)?([-.\s]?\d{1,9}){1,4}', description)

                if wa_match:
                    wa_number = wa_match.group(0)

                results.append((title, url, wa_number))
            except Exception as e:
                print(f"Failed to process result: {e}")

    except Exception as e:
        print(f"Error: {e}")
        
        # Capture screenshot for debugging
        driver.save_screenshot('screenshot.png')
        
        # Print page source for debugging
        page_source = driver.page_source
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(page_source)

    driver.quit()
    return results

def save_to_excel(data, filename='catering_results.xlsx'):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Catering Results'

    headers = ['Name', 'URL', 'WhatsApp Number']
    sheet.append(headers)

    for row in data:
        sheet.append(row)

    workbook.save(filename)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    query = 'nasi catering murah wa'
    search_results = fetch_google_results(query)

    if search_results:
        save_to_excel(search_results)
        print("Scraping and saving data completed successfully.")
    else:
        print("No results found or failed to fetch results.")
