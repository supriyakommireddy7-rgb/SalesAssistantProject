import os
import google.generativeai as genai
import json

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and api_key != 'your_gemini_api_key':
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_reply(self, email_body, customer_context=""):
        if not self.model:
            return None, 0.0
            
        system_prompt = """
        You are a highly professional real estate sales assistant.
        Your goal is to answer customer queries regarding real estate based on their email.
        Supported topics: Plot Price, Plot Location, Site Visit, Booking Process, Registration, Documentation, EMI, Loan, Maintenance, Profit Sharing, Greetings, Company Information.
        Do NOT invent prices. If you are unsure, provide a general polite response and state that a human executive will follow up.
        Provide your response in JSON format with two keys:
        1. "reply": The text of the reply.
        2. "confidence": A float between 0.0 and 1.0 indicating how confident you are in your answer based on the real estate context.
        """
        
        prompt = f"{system_prompt}\n\nCustomer Context: {customer_context}\n\nEmail Body: {email_body}"
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].strip()
                
            result = json.loads(text)
            return result.get('reply', "Thank you for reaching out. We will get back to you shortly."), float(result.get('confidence', 0.5))
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None, 0.0
