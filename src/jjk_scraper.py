import requests
from bs4 import BeautifulSoup 
import json
from tqdm import tqdm

wiki_url = 'https://jujutsu-kaisen.fandom.com'
characters = []

def scrape_character(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    name_element = soup.find('h1', class_='page-header__title')
    name = name_element.text.strip() if name_element else None
    
    img_element = soup.find('figure', class_='pi-item pi-image')
    image = img_element.img.get('src') if img_element and img_element.img else None
    
    abilities_section = soup.find('span', id='Abilities_and_Powers')
    abilities = []
    if abilities_section:
        abilities_list = abilities_section.find_next('ul')
        abilities = [ability.text.strip() for ability in abilities_list.find_all('li')]
    
    personality_section = soup.find('span', id='Personality')
    personality = personality_section.find_next('p').text.strip() if personality_section else None
    
    description_element = soup.find('div', {'id':'mw-content-text'}).find('p')
    description = description_element.text.strip() if description_element else None
    
    character = {
        'name': name,
        'image': image,
        'abilities': abilities,
        'personality': personality,
        'description': description
    }
                 
    characters.append(character)

def scrape_characters():
    category_url = f'{wiki_url}/wiki/Category:Characters'
    while category_url:
        res = requests.get(category_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        character_links = soup.select('.category-page__member-link')
        
        for link in tqdm(character_links, desc="Scraping characters", unit="character"):
            character_url = wiki_url + link['href']
            scrape_character(character_url)

        next_page = soup.find('a', string='Next page')   
        if next_page:
            category_url = wiki_url + next_page['href'] 
        else:
            category_url = None

scrape_characters()

with open('jjk_characters.json', 'w', encoding='utf-8') as f:
    json.dump(characters, f, ensure_ascii=False, indent=4, sort_keys=True)
