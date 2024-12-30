# NFC Tag Reader Backend with pyscard

This is a Flask application to read NFC tag data using pyscard and store it in an SQLite database.

## Files
- `app.py`: Flask application code, including NFC tag reading.
- `create_db.sql`: SQL script to create the necessary database table.

## Setup Instructions
1. Install Python and pip (if not already installed).
2. Install dependencies:
   ```bash
   pip install flask pyscard
   ```
3. Connect your NFC reader to the system.
4. Run the SQL script to set up the database:
   ```bash
   sqlite3 nfc_data.db < create_db.sql
   ```
5. Start the Flask server:
   ```bash
   python app.py
   ```

## API Usage
Send a POST request to `/api/nfc` to trigger NFC reading and store the tag ID.

## Example Response
Successful read:
```json
{
    "message": "Tag saved successfully!",
    "tag_id": "123ABC456"
}
```

Error reading NFC:
```json
{
    "error": "No NFC readers found"
}
```
