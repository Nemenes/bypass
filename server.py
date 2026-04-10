import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"
ENDPOINT = "https://bypass-production-a643.up.railway.app/webhook/ebay/deletion"

@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
def ebay_webhook():
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT
        challenge_response = base64.b64encode(
            hashlib.sha256(hash_input.encode()).digest()
        ).decode()

        return jsonify({"challengeResponse": challenge_response})

    data = request.json
    print("Received:", data)

    return "", 200


app.run(host="0.0.0.0", port=5000)