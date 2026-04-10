import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# MUST EXACTLY match what you entered in eBay Dev Portal
VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"

# MUST EXACTLY match the URL you entered in eBay Dev Portal
ENDPOINT = "https://bypass-production-a643.up.railway.app/webhook/ebay/deletion"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
@app.route("/webhook/ebay/deletion/", methods=["GET", "POST"])
def ebay_webhook():
    # --- Challenge verification (GET) ---
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        # eBay REQUIRED formula (no deviations)
        hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT
        print("HASH INPUT:", challenge_code + VERIFICATION_TOKEN + ENDPOINT)

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        return jsonify({
            "challengeResponse": challenge_response
        }), 200

    # --- Notification handling (POST) ---
    if request.method == "POST":
        # You can process/store deletion notice here if needed
        return "", 200

    return "", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
