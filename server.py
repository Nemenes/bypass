import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"
ENDPOINT = "bypass-production-a643.up.railway.app/webhook/ebay/deletion"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
def ebay_webhook():
    # --- Challenge verification ---
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        # MUST be exact order: challengeCode + verificationToken + endpoint
        hash_input = f"{challenge_code}{VERIFICATION_TOKEN}{ENDPOINT}"

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        return jsonify({"challengeResponse": challenge_response}), 200

    # --- Notification handling ---
    if request.method == "POST":
        data = request.get_json()
        print("Deletion event:", data)

        # You MUST return 200 within 3 seconds
        return "", 200

    return "", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)