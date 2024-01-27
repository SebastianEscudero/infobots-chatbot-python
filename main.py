import os
import json
import requests
from flask import Flask, request
from langchainBot import ask

app = Flask(__name__)
# Access token for your app
# (copy token from DevX getting started page
# and save it as an environment variable)

token = os.environ.get("WHATSAPP_TOKEN")


@app.route("/", methods=["GET"])
def index():
  return "Webhook is listening"


@app.route("/webhook", methods=["POST"])
def webhook():
  # Parse the request body from the POST
  body = request.get_json()

  # Check the Incoming webhook message
  print(json.dumps(body, indent=2))

  if body.get("object"):
    if (body.get("entry") and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]):
      phone_number_id = body["entry"][0]["changes"][0]["value"]["metadata"][
          "phone_number_id"]
      from_number = body["entry"][0]["changes"][0]["value"]["messages"][0][
          "from"]
      msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0][
          "text"]["body"]
      respuesta = ask(msg_body)
      payload = {
          "messaging_product": "whatsapp",
          "to": from_number,
          "text": {
              "body": respuesta
          }
      }
      print(payload)
      print(token)
      print(phone_number_id)
      url = f"https://graph.facebook.com/v17.0/184262751430193/messages?access_token={token}"
      headers = {"Content-Type": "application/json"}
      response = requests.post(url, json=payload, headers=headers)
      print(response)

  return "OK", 200


@app.route('/webhook', methods=['GET'])
def verificar_token():
  try:
    verifyToken = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if verifyToken == os.environ.get("VERIFY_TOKEN") and challenge != None:
      return challenge
    else:
      return 'token incorrecto', 403
  except Exception as e:
    return e, 403


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
