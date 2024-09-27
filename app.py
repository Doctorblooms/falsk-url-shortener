from flask import Flask, request, redirect, render_template, url_for
import hashlib
import os

app = Flask(__name__)


url_mapping = {}


def generate_short_url(original_url):
   
    hash_object = hashlib.sha1(original_url.encode())
    short_url = hash_object.hexdigest()[:5]  
    return short_url

@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html', url_mapping=url_mapping)

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    
    
    short_url = generate_short_url(original_url)

    
    url_mapping[short_url] = original_url
    
    
    return redirect(url_for('index'))

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    original_url = url_mapping.get(short_url)
    
    if original_url:
        return redirect(original_url)
    else:
        return "URL not found", 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port, debug=False)  