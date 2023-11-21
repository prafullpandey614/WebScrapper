import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_image_url(anchor_tag):
    if 'data-bg' in anchor_tag.attrs:
        img_url = anchor_tag['data-bg']
        return img_url
    return "xyz"

def extract_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        blog_posts = soup.find_all('div', class_='wrap')

        data = []  
        for post in blog_posts:
            try:
                title = post.find('div', class_='content').find('h6').find('a').text.strip()
                date_posted = post.find('div', class_='content').find('div', class_='blog-detail').find('div', class_='bd-item').find('span').text.strip()
                likes_cont = post.find('div', class_='content').find('a', class_="zilla-likes").find('span').text.strip()
                image_url = get_image_url(post.find('div', class_='img').find('a'))
                data.append({
                'Title': title,
                'Date Posted': date_posted,
                'Likes Count': likes_cont,
                'Image URL': image_url
            })
            except Exception as e:
                print("Some Exception occurred ",e)
            
            
                return data
        return data

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


base_url = "https://rategain.com/blog"
page_number = 1

all_data = []  


while True:
    target_url = f"{base_url}/page/{page_number}"
    print(f"Scraping data from page {page_number}...")
    
    page_data = extract_data(target_url)

    if page_data:
        all_data.extend(page_data)
        page_number += 1
    else:
        break

# Create a DataFrame from the list of data
df = pd.DataFrame(all_data)

excel_file_path = "scraped_data.xlsx"
df.to_excel(excel_file_path, index=False)

print(f"Data saved to {excel_file_path}")
