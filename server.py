import hashlib
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
@app.route("/webhook/ebay/deletion/", methods=["GET", "POST"])
def ebay_webhook():
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        # Force https (Railway fix)
        endpoint = request.url.replace("http://", "https://").split("?")[0]

        hash_input = f"{challenge_code}{VERIFICATION_TOKEN}{endpoint}"

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        return jsonify({"challengeResponse": challenge_response}), 200

    if request.method == "POST":
        data = request.get_json(silent=True)
        print("Deletion notification received:", data)
        return "", 200

    return "", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)