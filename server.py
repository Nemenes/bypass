import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# MUST match eBay Dev Portal EXACTLY
VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"

# MUST match eBay Dev Portal EXACTLY (NO trailing slash)
ENDPOINT = "https://bypass-production-a643.up.railway.app/webhook/ebay/deletion"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
@app.route("/webhook/ebay/deletion/", methods=["GET", "POST"])
def ebay_webhook():
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        # HARD GUARANTEE: remove any accidental trailing slash
        endpoint = ENDPOINT.rstrip("/")

        # eBay-required hash format
        hash_input = f"{challenge_code}{VERIFICATION_TOKEN}{endpoint}"

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        return jsonify({"challengeResponse": challenge_response}), 200

    if request.method == "POST":
        return "", 200

    return "", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
