# Automatic Email Reply System  
This project is an **automatic mail responder** that:  
1. Reads unread emails from Gmail using the **Gmail API**  
2. Extracts relevant details (sender, subject, body)  
3. Generates a professional reply using **Gemini API (Google AI)**  
4. Sends the reply automatically using Gmail API  

---

## **Features**
- **Automated Email Fetching** – continuously monitors the inbox  
- **AI-Powered Replies** – leverages Gemini to generate polite, context-aware responses  
- **Secure API Key Handling** – uses `.env` file to store secrets securely  
- **Single Sender Filter** – currently configured to respond only to specific senders  
- **Duplicate Protection** – prevents replying multiple times to the same email  

---

## **Tech Stack**
- **Language:** Python  
- **APIs:** 
  - [Gmail API](https://developers.google.com/gmail/api)  
  - [Gemini API](https://ai.google.dev/)  
- **Authentication:** OAuth 2.0 (via Gmail API)  
- **Environment Management:** `python-dotenv`  

---

## **How It Works**
1. **Authenticate with Gmail API** – using OAuth and a `token.json` file  
2. **Check Inbox for Unread Mails** – via Gmail API query `is:unread`  
3. **Filter Sender** – only trigger replies for specific email addresses (can be customized)  
4. **Generate Reply with Gemini API** – prompts Gemini to return a structured JSON with reply subject & body  
5. **Send the Reply Email** – Gmail API sends the email automatically  

---
## Future Improvements
- **Optimize the Process** – streamline email fetching, AI reply generation, and sending to reduce latency and improve efficiency  
- **Database Integration** – connect the system to a database to store and manage email data persistently  
- **User-Specific Email Tracking** – keep track of emails for each user separately to provide a more personalized and unique response experience  

