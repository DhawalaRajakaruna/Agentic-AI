from google import genai
from dotenv import load_dotenv
import os
import json


def Generatemail(email_address, subject, body):
    # Load the API key from .env file
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Build a clear prompt for Gemini
    prompt = f"""
    You are an AI assistant. A person sent me this email:

    From: {email_address}
    Subject: {subject}
    Body: {body}
    use My name as Rajakaruna.R.W.M.D.S

    Please write a professional and polite email reply.
    Return your response strictly as a JSON object in the following format:
    {{
      "isreply": true,
      "replyto": "{email_address}",
      "replysubject": "<subject of the reply>",
      "replybody": "<body of the reply>"
    }}
    Do not include any extra text outside the JSON object.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        data = json.loads(response.text)
        isreply = data.get("isreply")
        replyto = data.get("replyto")
        resubject = data.get("replysubject")
        rebody = data.get("replybody")
    except json.JSONDecodeError:
        # If Gemini adds extra text, extract JSON manually
        text = response.text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        data = json.loads(json_text)
        isreply = data.get("isreply")
        replyto = data.get("replyto")
        resubject = data.get("replysubject")
        rebody = data.get("replybody")

    # Return all four variables
    return isreply, replyto, resubject, rebody

