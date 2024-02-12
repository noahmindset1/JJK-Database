import requests
from bs4 import BeautifulSoup 
import sqlite3
from tqdm import tqdm
import json

# Establishing connection to SQLite database
conn = sqlite3.connect('jjk_characters.db')
c = conn.cursor()

# Creating Characters table
c.execute('''CREATE TABLE IF NOT EXISTS Characters
             (id INTEGER PRIMARY KEY,
              name TEXT,
              image TEXT,
              abilities TEXT,
              personality TEXT,
              description TEXT)''')

wiki_url = 'https://jujutsu-kaisen.fandom.com'

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
    
    # Inserting data into the Characters table
    c.execute("INSERT INTO Characters (name, image, abilities, personality, description) VALUES (?, ?, ?, ?, ?)",
              (name, image, json.dumps(abilities), personality, description))
    conn.commit()

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

# Closing the connection to the SQLite database
conn.close()

