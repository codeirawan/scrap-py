import requests
from bs4 import BeautifulSoup
import json

# Function to fetch a web page using requests
def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch {url}, Status code: {response.status_code}")
        return None

# Function to scrape topics from Alodokter community page and get only URLs
def scrape_topics(url):
    page_content = fetch_page(url)
    if not page_content:
        print(f"Failed to fetch page: {url}")
        return []

    soup = BeautifulSoup(page_content, 'html.parser')
    print(soup.prettify())
    urls = []

    # Find all topic elements
    topic_elements = soup.find_all('li', class_='index-item')

    for topic_elem in topic_elements:
        topic_url = 'https://www.alodokter.com' + topic_elem.find('a')['href']
        urls.append(topic_url)

    return urls

# Function to scrape topics from Alodokter community page
def scrape_topicsx(url):
    page_content = fetch_page(url)
    if not page_content:
        print(f"Failed to fetch page: {url}")
        return []

    soup = BeautifulSoup(page_content, 'html.parser')
    topics = []

    # Try finding topic elements directly without complex CSS selector
    topic_elements = soup.find_all(class_='index-item')

    print(topic_elements)

    if not topic_elements:
        print(f"No topics found on page: {url}")
        return []

    for topic_elem in topic_elements:
        topic_title = topic_elem.text.strip()
        topic_url = 'https://www.alodokter.com' + topic_elem.find('a')['href']
        topics.append({
            'title': topic_title,
            'url': topic_url
        })

    return topics

# Function to scrape discussions from a specific topic page
def scrape_discussions(url):
    page_content = fetch_page(url)
    if not page_content:
        return []

    soup = BeautifulSoup(page_content, 'html.parser')
    discussions = []

    discussion_elements = soup.find_all('div', class_='list-item-topic')
    for discussion_elem in discussion_elements:
        discussion_title = discussion_elem.find('h4', class_='title').text.strip()
        discussion_url = 'https://www.alodokter.com' + discussion_elem.find('a')['href']
        discussions.append({
            'title': discussion_title,
            'url': discussion_url
        })

    return discussions

# Function to scrape question and answer details from a discussion page
def scrape_question_answer(url):
    page_content = fetch_page(url)
    if not page_content:
        return None

    soup = BeautifulSoup(page_content, 'html.parser')

    # Extracting topic tags
    topic_tags = soup.find('ul', class_='topic-tags')
    if topic_tags:
        topic_text = ', '.join(tag.text.strip() for tag in topic_tags.find_all('li'))
    else:
        topic_text = ''

    # Extracting title, question, answer, and doctor's name
    title = soup.find('h1', class_='title-topic').text.strip()
    question = soup.find('div', class_='question').text.strip()
    answer = soup.find('div', class_='answer').text.strip()
    doctor = soup.find('span', class_='doctor-name').text.strip()

    data = {
        'topic': topic_text,
        'title': title,
        'question': question,
        'answer': answer,
        'doctor': doctor,
        'url': url
    }

    return data

if __name__ == "__main__":
    base_url = 'https://www.alodokter.com/komunitas/topik'
    topics = scrape_topics(base_url)

    all_data = []

    if topics:
        print("Topics found:")
        for topic in topics:
            print(f"Title: {topic['title']}")
            print(f"URL: {topic['url']}")
            print()
    else:
        print("No topics found or failed to fetch topics.")

    for topic in topics:
        topic_url = topic['url']
        print(f"Scraping discussions from topic: {topic['title']} - {topic_url}")
        discussions = scrape_discussions(topic_url)

        if not discussions:
            print(f"No discussions found for topic: {topic['title']}")
            continue

        for discussion in discussions:
            discussion_url = discussion['url']
            print(f"Scraping details from discussion: {discussion['title']} - {discussion_url}")
            discussion_data = scrape_question_answer(discussion_url)

            if discussion_data:
                # Add additional information to discussion_data
                discussion_data['topic'] = topic['title']  # Add topic title
                discussion_data['url'] = discussion_url    # Add discussion URL

                all_data.append(discussion_data)
            else:
                print(f"No data scraped for discussion: {discussion['title']}")

    # Saving data to JSON file
    with open('alodokter_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print("Scraping completed. Data saved to alodokter_data.json")
