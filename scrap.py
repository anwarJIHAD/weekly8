import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://lxegydya:admin@cluster0.s4ymqoi.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.lxdb

data = requests.get('https://www.bilibili.tv/id/anime')
soup = BeautifulSoup(data.text, 'html.parser')

animes = soup.select('.bstar-video-card')

for anime in animes:
    title = anime.select_one('.bstar-video-card__title-text').text.strip()
    genre = anime.select_one('.bstar-video-card__desc').text.strip().replace('Â', '').split('·').pop().strip()
    cover = anime.select_one('.bstar-image__img').get('src').split('@')[0]

    doc = {
        'title' : title,
        'genre' : genre,
        'cover' : cover
    }

    db.anime_list.insert_one(doc)

print(list(db.anime_list.find()))