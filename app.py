from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Replace this with your publicly accessible URL of your internal server
# Example: http://<your-public-ip>:5000 or the ngrok URL
INTERNAL_APP_URL = "http://130.61.62.250:5001"

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    # Construct the full URL to forward to
    url = f"{INTERNAL_APP_URL}/{path}"
    
    # Forward the request
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # Build the Flask response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
