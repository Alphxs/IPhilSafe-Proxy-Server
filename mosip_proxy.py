import os
import requests
import warnings
from flask import Flask, request, jsonify

warnings.filterwarnings("ignore")  # suppress InsecureRequestWarning

app = Flask(__name__)

MOCK_URL = "https://cs145-iot-cup-1745973870.ap-southeast-1.elb.amazonaws.com"

@app.route("/api/v1/auth/<path:endpoint>", methods=["POST"])
def proxy(endpoint):
    resp = requests.post(
        f"{MOCK_URL}/api/v1/auth/{endpoint}",
        json=request.get_json(),
        verify=False,
    )
    print(f"Mock server status: {resp.status_code}")
    print(f"Mock server body: {repr(resp.text)}")
    
    if not resp.text.strip():
        return jsonify({"error": "Mock server returned empty response", "status_code": resp.status_code}), 502
    
    try:
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e), "raw": resp.text}), 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)