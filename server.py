import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# MUST match what you entered in eBay dev portal
VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
@app.route("/webhook/ebay/deletion/", methods=["GET", "POST"])
def ebay_webhook():
    # --- Challenge verification (GET) ---
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        # Dynamically get exact URL eBay is calling (prevents mismatch issues)
        endpoint = request.url.split("?")[0]

        # Required hash: challengeCode + verificationToken + endpoint
        hash_input = f"{challenge_code}{VERIFICATION_TOKEN}{endpoint}"

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        return jsonify({"challengeResponse": challenge_response}), 200

    # --- Notification handling (POST) ---
    if request.method == "POST":
        data = request.get_json(silent=True)
        print("Deletion notification received:", data)

        # Must return 200 within 3 seconds
        return "", 200

    return "", 400


if __name__ == "__main__":
    # Required for Railway / cloud hosting
    app.run(host="0.0.0.0", port=5000)