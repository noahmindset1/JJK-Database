import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

wiki_url = 'https://jujutsu-kaisen.fandom.com'
items = []

categories = [
    'Characters',
    'Episodes',
    'Soundtrack',
    'Volumes_&_Chapters'  
]

def scrape_page(url, title_element_class='page-header__title', image_element_class='pi-item pi-image'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title_element = soup.find('h1', class_=title_element_class)
    title = title_element.text.strip() if title_element else None
    
    img_element = soup.find('figure', class_=image_element_class)
    image = img_element.img.get('src') if img_element and img_element.img else None
    
    details = {}
    for detail in soup.find_all('div', class_='pi-item'):
        key = detail.find(class_='pi-data-label')
        value = detail.find(class_='pi-data-value')
        if key and value:
            details[key.text.strip()] = value.text.strip()
            
    abilities_section = soup.find('span', id='Abilities_and_Powers')
    abilities = []
    if abilities_section:
        abilities_list = abilities_section.find_next('ul')
        abilities = [ability.text.strip() for ability in abilities_list.find_all('li')]
    
    personality_section = soup.find('span', id='Personality')
    personality = personality_section.find_next('p').text.strip() if personality_section else None
    
    description_element = soup.find('div', {'id':'mw-content-text'}).find('p')
    description = description_element.text.strip() if description_element else None
    
    voice_actors = []
    voice_actor_section = soup.find('span', id='Voice_Actors')
    if voice_actor_section:
        voice_actors_list = voice_actor_section.find_next('ul')
        voice_actors = [actor.text.strip() for actor in voice_actors_list.find_all('li')]
        
    additional_info = {}
    for div in soup.find_all('div', class_='pi-item'): 
        label = div.find(class_='pi-data-label')
        value = div.find(class_='pi-data-value')
        if label and value:
            additional_info[label.text.strip()] = value.text.strip()
            
    item = {
        'title': title,
        'image': image,
        'details': details,
        'abilities': abilities,
        'personality': personality,
        'description': description,
        'voice_actors': voice_actors,
        'additional_info': additional_info
    }
                 
    items.append(item)
       
def scrape_category(category):
    category_url = f'{wiki_url}/wiki/Category:{category}'    
    res = requests.get(category_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    item_links = soup.select('.category-page__member-link')
        
    for link in tqdm(item_links, desc=f"Scraping {category}", unit="item"):
        item_url = wiki_url + link['href']
        scrape_page(item_url)

    next_page = soup.find('a', string='Next page')    
    if next_page:
        next_page_url = wiki_url + next_page['href'] 
        scrape_category(next_page_url)
        
for category in categories:
    scrape_category(category)
    
with open('jujutsu_kaisen_data.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=4)
