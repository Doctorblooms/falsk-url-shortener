from flask import Flask, request, redirect, render_template, url_for
import string
import random

app = Flask(__name__)

# Dictionary to store shortened URLs
url_mapping = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()

        # Ensure the short code is unique
        while short_code in url_mapping:
            short_code = generate_short_code()

        # Store mapping
        url_mapping[short_code] = original_url

        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_url(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return '<h1>URL not found</h1>', 404

if __name__ == '__main__':
    app.run(debug=True)
