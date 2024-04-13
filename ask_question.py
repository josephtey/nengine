import modal


stub = modal.Stub()
from lib.nengine.nengine import NotesEngine  # auto-dependency

stub_image = modal.Image.debian_slim(python_version="3.9").run_commands(
    "apt-get update",
    "pip install twilio openai",
)

path = "/Users/josephtey/Library/Mobile Documents/iCloud~md~obsidian/Documents/Life/Transient Notes"


@stub.function(
    schedule=modal.Period(days=1),
    image=stub_image,
    mounts=[modal.Mount.from_local_dir(path, remote_path="/root/notes")],
    secrets=[modal.Secret.from_name("nengine")],
)
def ask_question():
    from twilio.rest import Client
    import os
    from openai import OpenAI
    from lib.nengine.nengine import NotesEngine

    local_path = "/root/notes"

    engine = NotesEngine(local_path)
    files = engine.get_files()

    # files = get_files(local_path, None)
    random_file = engine.pick_random_file(files)

    if random_file:
        full_path = os.path.join(local_path, random_file)
        file_content = engine.read_file_content(full_path)

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ["OPENAI_API_KEY"],
    )

    prompt = """
      After reading the following reflection, ask a 1-sentence question. The question should be short, direct, use simple language, and can be one of three types: 
      1. If you disagree, critique this reflection with an honest, direct question. 
      2. If you agree, ask a question about what you found insightful. 
      3. If you are unsure, ask a 1-sentence question that you would ask to clarify. 

      Here is the reflection:
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Critique this reflection with an honest, direct 1-sentence question:"
                + file_content,
            }
        ],
        model="gpt-4-turbo",
    )

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=os.environ["TWILIO_WHATSAPP_FROM"],
        body=chat_completion.choices[0].message.content
        + "\n\n"
        + "Source: "
        + random_file[:-3],
        to=os.environ["TWILIO_WHATSAPP_TO"],
    )

    print("Success!")
