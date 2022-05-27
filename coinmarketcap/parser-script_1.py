import sqlite3
from bs4 import BeautifulSoup
import requests


connection = sqlite3.connect("crypto_db.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS crypto_data(
                    id INT PRIMARY KEY NOT NULL,
                    crypto_name TEXT NOT NULL,
                    market_cap TEXT NOT NULL,
                    circulating_supply TEXT NOT NULL);
                    """)

for i in range(1, 6):
    url = f"https://coinmarketcap.com/?page={i}"
    r = requests.get(url)
    c = r.text
    soup = BeautifulSoup(c, 'html.parser')
    table = soup.find_all("tbody")[0]
    table_rows = table.find_all("tr")
    for table_row in table_rows:
        row_items = table_row.find_all("p")
        if len(row_items) > 5:
            index_value_map = {0: "id", 1: "crypto_name", 3: "market_cap", 6: "circulating_supply"}
            cursor.execute("INSERT INTO crypto_data (id, crypto_name, market_cap, circulating_supply) VALUES (?, ?, ?, ?)",
                           (row_items[0].get_text(), row_items[1].get_text(), row_items[3].get_text(), row_items[6].get_text()))
            connection.commit()

cursor.close()
connection.close()