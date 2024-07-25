from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Path to your ChromeDriver
CHROMEDRIVER_PATH = 'D:\\code\\scrap\\chromedriver-win32\\chromedriver.exe'

# URL of the Google Maps reviews page
URL = 'https://www.google.com/maps/place/PT+Bridge+Note+Indonesia/@-6.2313707,106.8250435,920m/data=!3m1!1e3!4m8!3m7!1s0x2e69f3b6e9474b9f:0xd9c60e44b16cc7f7!8m2!3d-6.2313707!4d106.8276184!9m1!1b1!16s%2Fg%2F11sv7btpd8?entry=ttu'

def fetch_reviews(url):
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    reviews = []  # Initialize reviews list before try block
    unique_reviews = set()  # To keep track of unique reviews

    try:
        driver.get(url)
        print("Page loaded.")

        # Wait until reviews are present
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-review-id]'))
        )
        print("Reviews section found.")

        # Find review elements
        review_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')

        print(f"Found {len(review_elements)} reviews.")

        for review in review_elements:
            try:
                author_name = review.find_element(By.CSS_SELECTOR, 'div.d4r55').text.strip()
                rating_element = review.find_element(By.CSS_SELECTOR, 'span.kvMYJc')
                rating = rating_element.get_attribute('aria-label').strip() if rating_element else 'No Rating'
                date = review.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text.strip()
                comment = review.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text.strip()

                # Create a unique identifier for the review
                review_id = (author_name, rating, date, comment)

                # Add review if it's not a duplicate
                if review_id not in unique_reviews:
                    unique_reviews.add(review_id)
                    reviews.append([author_name, rating, date, comment])
            except Exception as e:
                print(f"Error extracting review: {e}")

    except Exception as e:
        print(f"Error loading page or finding reviews: {e}")

    finally:
        driver.quit()

    return reviews

def save_reviews_to_csv(reviews, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Author Name', 'Rating', 'Date', 'Comment'])
        
        for review in reviews:
            writer.writerow(review)
    
    print(f'Reviews have been saved to {filename}')

if __name__ == '__main__':
    reviews = fetch_reviews(URL)
    if reviews:
        save_reviews_to_csv(reviews, 'google_reviews.csv')
    else:
        print("No reviews found.")
