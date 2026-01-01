from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

VULNERABLE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Image Fetcher</title>
</head>
<body>
    <h1>Fetch an Image</h1>
    <form action="/fetch" method="get">
        URL: <input type="text" name="url" placeholder="http://example.com/image.jpg">
        <input type="submit" value="Fetch">
    </form>
    <div id="result">
        {% if content %}
            <h2>Fetched Content:</h2>
            <pre>{{ content }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(VULNERABLE_TEMPLATE)

@app.route("/fetch")
def fetch():
    target_url = request.args.get("url")
    if not target_url:
        return "URL parameter is missing", 400
    
    try:
        # Intentionally vulnerable to SSRF
        response = requests.get(target_url, timeout=5)
        return render_template_string(VULNERABLE_TEMPLATE, content=response.text)
    except Exception as e:
        return render_template_string(VULNERABLE_TEMPLATE, content=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
