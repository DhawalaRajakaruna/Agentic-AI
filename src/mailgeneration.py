from langchain_ollama import OllamaLLM  # Updated class
from langchain.memory import ConversationSummaryMemory
import json
import re

# Initialize memory globally so it persists across multiple email generations
memory = ConversationSummaryMemory(
    llm=OllamaLLM(model="llama3"),  # Use the same LLM for summarization
    memory_key="chat_history",
    input_key="input",
    output_key="output"
)

def createmail(email_address, subject, body):
    print("Generating the reply mail ...")
    
    # Include previous conversation summary in the prompt
    previous_summary = memory.load_memory_variables({})["chat_history"]
    
    llm = OllamaLLM(model="llama3")  # Use llama3
    
    prompt = f"""
    Previous Emails Summary:
    {previous_summary}

    Generate a professional email reply.

    Original Email:
    From: {email_address}
    Subject: {subject}
    Body: {body}

    Instructions:
    - Write a polite and professional reply.
    - Include my name at the end: Dhawala Sanka Rajakaruna
    - Return ONLY the following JSON format, nothing else:

    {{
    "subject": "<reply subject>",
    "body": "<reply body>"
    }}
    """

    
    # Generate the response using the LLM
    response = llm.invoke(prompt)

    # Update memory with the new message (original + reply)
    memory.save_context(
        {"input": f"From: {email_address}\nSubject: {subject}\nBody: {body}"},
        {"output": response}
    )



    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        try:
            response_json = json.loads(json_str)
            reply_subject = response_json.get("subject", "")
            reply_body = response_json.get("body", "")
            return reply_subject, reply_body
        except json.JSONDecodeError:
            print("Error parsing JSON:", json_str)
            return None, None
    else:
        print("No JSON found in response:", response)
        return None, None

    
