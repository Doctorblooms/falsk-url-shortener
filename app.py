from flask import Flask, request, redirect, render_template, url_for
import string
import os

app = Flask(__name__)

# In-memory storage for shortened URLs
url_mapping = {}
next_id = 0  # This will keep track of the next ID for encoding

# Base62 characters
BASE62 = string.ascii_letters + string.digits
BASE = len(BASE62)

def encode(num):
    """Convert a number to a base62 string."""
    if num == 0:
        return BASE62[0]
    
    arr = []
    while num > 0:
        num, rem = divmod(num, BASE)
        arr.append(BASE62[rem])
    return ''.join(reversed(arr))

def decode(short_url):
    """Convert a base62 string back to a number."""
    num = 0
    for char in short_url:
        num = num * BASE + BASE62.index(char)
    return num

@app.route('/', methods=['GET'])
def index():
    # Pass url_mapping to the template
    return render_template('index.html', url_mapping=url_mapping)

@app.route('/shorten', methods=['POST'])
def shorten():
    global next_id  # Use global variable to track the next ID
    original_url = request.form['url']
    
    # Generate a short URL using base62 encoding
    short_url = encode(next_id)
    next_id += 1  # Increment the ID for the next short URL

    # Store the mapping
    url_mapping[short_url] = original_url
    
    # Redirect to the index after shortening
    return redirect(url_for('index'))

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    original_url = url_mapping.get(short_url)
    
    if original_url:
        return redirect(original_url)
    else:
        return "URL not found", 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not specified
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
