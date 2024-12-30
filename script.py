import sqlite3
import random
from datetime import datetime, timedelta

# Top 100 ATP player names (as of recent data)
atp_players = [
    "Novak Djokovic", "Carlos Alcaraz", "Daniil Medvedev", "Jannik Sinner", "Andrey Rublev",
    "Stefanos Tsitsipas", "Alexander Zverev", "Holger Rune", "Taylor Fritz", "Casper Ruud",
    "Hubert Hurkacz", "Frances Tiafoe", "Grigor Dimitrov", "Karen Khachanov", "Tommy Paul",
    "Felix Auger-Aliassime", "Ben Shelton", "Cameron Norrie", "Alex De Minaur", "Lorenzo Musetti",
    "Francisco Cerundolo", "Adrian Mannarino", "Alexander Bublik", "Sebastian Korda", "Jan-Lennard Struff",
    "Ugo Humbert", "Tallon Griekspoor", "Alejandro Davidovich Fokina", "Nicolas Jarry", "Matteo Berrettini",
    "Daniel Evans", "Milos Raonic", "Borna Coric", "Aslan Karatsev", "Christopher Eubanks",
    "Lorenzo Sonego", "Maxime Cressy", "Jiri Lehecka", "Denis Shapovalov", "Emil Ruusuvuori",
    "Arthur Fils", "Roberto Bautista Agut", "Dominic Thiem", "Brandon Nakashima", "Jordan Thompson",
    "Stan Wawrinka", "Yibing Wu", "Andy Murray", "Diego Schwartzman", "Marton Fucsovics",
    "Sebastian Baez", "Mackenzie McDonald", "John Isner", "Jack Draper", "Laslo Djere",
    "Yoshihito Nishioka", "Richard Gasquet", "Marc-Andrea Huesler", "Pedro Cachin", "Tomas Martin Etcheverry",
    "Marcos Giron", "J.J. Wolf", "Gregoire Barrere", "Benjamin Bonzi", "Gael Monfils",
    "Dusan Lajovic", "Albert Ramos-Vinolas", "Fabio Fognini", "Jaume Munar", "Thiago Monteiro",
    "Alexei Popyrin", "Brandon Holt", "Aleksandar Kovacevic", "Pablo Carreno Busta", "Dominic Stricker",
    "Botic van de Zandschulp", "Radu Albot", "Michael Mmoh", "Jason Kubler", "Daniel Altmaier",
    "Taro Daniel", "Christopher O'Connell", "Thanasi Kokkinakis", "Luca Nardi", "Facundo Diaz Acosta",
    "Liam Broady", "Denis Kudla", "Hugo Dellien", "Alexander Shevchenko", "Zizou Bergs"
]

# Generate random timestamps starting from 2024
def random_timestamp():
    start_date = datetime(2024, 1, 1)
    random_days = random.randint(0, 365)  # Random day within the year 2024
    random_time = timedelta(seconds=random.randint(0, 86400))  # Random time within the day
    return (start_date + timedelta(days=random_days) + random_time).strftime('%Y-%m-%d %H:%M:%S')

# Create database and table
conn = sqlite3.connect('nfc_data.db')
c = conn.cursor()

# Ensure table exists before deletion
c.execute('''CREATE TABLE IF NOT EXISTS tags (
    name TEXT,
    tag_id TEXT,
    timestamp TEXT
)''')

# Delete all rows from tags table
c.execute('''DELETE FROM tags''')

# Recreate tags table (optional drop for clean state)
c.execute('''DROP TABLE IF EXISTS tags''')
c.execute('''CREATE TABLE tags (
    name TEXT,
    tag_id TEXT,
    timestamp TEXT
)''')

# Insert 3000 rows with random player names, tag_ids, and timestamps
for _ in range(3000):
    name = random.choice(atp_players)
    tag_id = f"TAG-{random.randint(1000, 9999)}"
    timestamp = random_timestamp()
    c.execute('INSERT INTO tags (name, tag_id, timestamp) VALUES (?, ?, ?)', (name, tag_id, timestamp))

# Commit and close
conn.commit()
conn.close()

print("Database 'nfc_data.db' with table 'tags' created and populated successfully.")
