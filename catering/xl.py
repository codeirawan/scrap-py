import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Request Status Code: {response.status_code}")  # Print status code for debugging
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Dapatkan hasil pencarian (sesuaikan dengan struktur HTML aktual dari Google)
    search_results = soup.find_all("div", class_="g")  # Sesuaikan dengan class atau atribut yang sesuai
    
    print(f"Number of search results found: {len(search_results)}")  # Print number of search results found for debugging
    
    # List untuk menyimpan hasil yang akan dikembalikan
    scraped_data = []
    
    # Proses dan analisis hasil sesuai dengan struktur HTML dari Google
    for result in search_results:
        try:
            # Lakukan pemrosesan yang diperlukan untuk mendapatkan data harga catering
            title = result.find("h3").get_text()  # Contoh: mendapatkan teks dari tag <h3> untuk judul
            link = result.find("a")["href"]  # Contoh: mendapatkan atribut href dari tag <a> untuk link
            
            # Tambahkan ke list scraped_data
            scraped_data.append({"Title": title, "Link": link})
        
        except Exception as e:
            print(f"Error processing result: {e}")
    
    # Return scraped_data, atau sesuaikan dengan apa yang ingin Anda kembalikan
    return scraped_data

def save_to_excel(data, filename="scraped_data.xlsx"):
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data)
    
    # Save DataFrame to Excel
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename} successfully.")

if __name__ == "__main__":
    query = "catering area jakarta harga 10-15rb"
    results = scrape_google(query)
    
    if results:
        print(f"Number of results retrieved: {len(results)}")
        print(results)
        
        # Save results to Excel
        save_to_excel(results)
    else:
        print("No results retrieved.")
