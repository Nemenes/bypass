import hashlib
import base64
from flask import Flask, request, Response

app = Flask(__name__)

VERIFICATION_TOKEN = "gyuidfiugdfiugiudfgdifoguasasdasd"
ENDPOINT = "https://bypass-production-a643.up.railway.app/webhook/ebay/deletion"


@app.route("/webhook/ebay/deletion", methods=["GET", "POST"])
@app.route("/webhook/ebay/deletion/", methods=["GET", "POST"])
def ebay_webhook():
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT

        digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
        challenge_response = base64.b64encode(digest).decode("utf-8")

        body = f'{{"challengeResponse":"{challenge_response}"}}'

        return Response(
            response=body,
            status=200,
            mimetype="application/json"
        )

    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
