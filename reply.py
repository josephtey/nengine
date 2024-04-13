from modal import Stub, wsgi_app, Image, Secret

stub = Stub()

stub_image = Image.debian_slim(python_version="3.9").run_commands(
    "apt-get update",
    "pip install twilio flask",
)


@stub.function(
    image=stub_image,
    secrets=[Secret.from_name("nengine")],
)
@wsgi_app()
def reply():
    from flask import Flask, request
    from twilio.twiml.messaging_response import MessagingResponse

    print("ACTIVATED #111!")
    web_app = Flask(__name__)

    @web_app.post("/sms")
    def home():
        print("ACTIVATEDDD!")
        body = request.values.get("Body", None)
        print(body)
        # Start our TwiML response
        resp = MessagingResponse()

        # Determine the right reply for this message
        if body == "hello":
            print("you said hello")
            resp.message("Hi!")
        elif body == "bye":
            print("you said bye")
            resp.message("Goodbye")

        return str(resp)

        # import os
        # from twilio.rest import Client

        # account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        # client = Client(account_sid, auth_token)

        # print(str(item))

        # message = client.messages.create(
        #     from_=os.environ["TWILIO_WHATSAPP_FROM"],
        #     body="Hello",
        #     to=os.environ["TWILIO_WHATSAPP_TO"],
        # )
