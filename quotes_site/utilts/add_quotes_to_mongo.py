import json 
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client.hw
try:
    client.admin.command('ping')
    print("Підключення до MongoDB успішне")
except Exception as e:
    print("Помилка підключення до MongoDB:", e)


with open('quotes.json', 'r', encoding='utf-8') as fd:
        quotes = json.load(fd)
        print(quotes)
    
for quote in quotes:
    try:
        author = db.authors.find_one({'fullname': quote['author']})
        if author:
            db.quotes.insert_one({
                'quote': quote['quote'],
                'tags': quote['tags'],
                'author': ObjectId(author['_id'])
            })
            print(f"Цитата від {quote['author']} додана.")
        else:
            print(f"Автор {quote['author']} не знайдений.")
    except Exception as e:
        print(f"Помилка при вставці цитати: {e}")
