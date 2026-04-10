import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# MUST exactly match what you set in eBay Dev Portal
VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"

# MUST exactly match (NO trailing slash)
ENDPOINT = "https://bypass-production-a643.up.railway.app/webhook/ebay/deletion"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
@app.route("/webhook/ebay/deletion/", methods=["GET", "POST"])
def ebay_webhook():
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        # STRICT eBay formula
        hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT

        # Debug (remove later if you want)
        print("HASH INPUT:", hash_input)

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        return jsonify({"challengeResponse": challenge_response}), 200

    # POST notifications
    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
