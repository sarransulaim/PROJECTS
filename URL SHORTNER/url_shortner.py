from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random

app = Flask(__name__, template_folder='templates', static_folder='staticfiles')


# Connect to SQLite database
conn = sqlite3.connect('url_shortener.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY, long_url TEXT, short_code TEXT)''')
conn.commit()

conn.close()

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    
    # Check if URL already exists in the database
    c.execute("SELECT short_code FROM urls WHERE long_url=?", (long_url,))
    row = c.fetchone()
    if row:
        short_code = row[0]
    else:
        # Generate a new short code
        short_code = generate_short_code()
        # Insert new URL into database
        c.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
        conn.commit()
    
    conn.close()
    
    # Construct the shortened URL relative to the application's root
    shortened_url = f"/{short_code}"
    
    # Pass the shortened URL to the template
    return render_template("index.html", shortened_url=shortened_url)



@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    
    # Retrieve long URL from short code
    c.execute("SELECT long_url FROM urls WHERE short_code=?", (short_code,))
    row = c.fetchone()
    
    if row:
        long_url = row[0]
        conn.close()
        return redirect(long_url)
    else:
        conn.close()
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
