from flask import Flask, request, redirect, render_template, url_for
import hashlib
import os

app = Flask(__name__)

# In-memory storage for shortened URLs
url_mapping = {}

# Function to generate a short URL using SHA-1 hashing
def generate_short_url(original_url):
    # Create a SHA-1 hash of the original URL
    hash_object = hashlib.sha1(original_url.encode())
    short_url = hash_object.hexdigest()[:5]  # Take the first 5 characters of the hash
    return short_url

@app.route('/', methods=['GET'])
def index():
    # Pass url_mapping to the template
    return render_template('index.html', url_mapping=url_mapping)

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    
    # Generate a short URL using the SHA-1 hash
    short_url = generate_short_url(original_url)

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
