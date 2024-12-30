import time
import sqlite3
from datetime import datetime
import subprocess
from flask import Flask
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from threading import Thread

app = Flask(__name__)

# Database connection setup
DATABASE = 'nfc_data.db'


# Create table in SQLite database
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id TEXT NOT NULL UNIQUE,
            name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sportivi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_name_from_sportivi(tag_id):
    # Query the sportivi table to get the name based on tag_id
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sportivi WHERE tag_id = ?', (tag_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # Return the name found in the sportivi table
    else:
        return "Unknown"  # Return Unknown if tag_id not found


def save_tag_info(tag_id, name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO tags (tag_id, name, timestamp) VALUES (?, ?, ?)', (tag_id, name, timestamp))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Tag {tag_id} already exists in the database.")
    finally:
        conn.close()

    print(f"Saved {tag_id} with name '{name}' and timestamp {timestamp}.")


# Function to read NFC tags
def read_nfc_tag():
    print(get_name_from_sportivi("EB27623D"))
    while True:
        try:
            r = readers()
            if not r:
                print("No readers found")
                time.sleep(1)
                continue
            reader = r[0]
            connection = reader.createConnection()
            connection.connect()

            # Read tag UID (modify if necessary for your NFC reader)
            SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = connection.transmit(SELECT)
            tag_id = ''.join(format(x, '02X') for x in data)
            # Lookup name from the sportivi table
            name = get_name_from_sportivi(tag_id)
            print(tag_id, name)
            if name != "Unknown":
                save_tag_info(tag_id, name)
                print(f"Tag {tag_id} scanned. Name: {name}")

            time.sleep(2)  # Prevent rapid looping for the same tag

        except NoCardException:
            time.sleep(0.37)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.37)


# Function to run Git commands at every 10-minute mark (i.e., when seconds == 0)
def run_git_commands():
    while True:
        # Get the current time
        current_time = datetime.now()

        # Check if the current minute is divisible by 10 and the seconds are 0
        if current_time.minute % 10 == 0 and current_time.second == 0:
            try:
                # Run Git commands
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
                subprocess.run(["git", "push", "heroku", "master"], check=True)
                print("Git commands executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error during Git command execution: {e}")

            # Sleep for 60 seconds to avoid running again during the same 10-minute window
            time.sleep(60)
        else:
            # Sleep for a short time to avoid checking constantly
            time.sleep(1)


if __name__ == "__main__":
    print("Starting NFC tag reader...")
    create_table()  # Set up the database table
    # Run both the NFC tag reader and Git commands function concurrently
    nfc_thread = Thread(target=read_nfc_tag)
    nfc_thread.start()

    git_thread = Thread(target=run_git_commands)
    git_thread.start()
