import os
import requests

class OpenAIClient:
    def __init__(self):
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.api_key = "YOUR_OPENAI_API_KEY"

    def chat_completion(self, messages, model="meta/llama-3.1-405b-instruct", temperature=0.7, max_tokens=200):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error in API request: {str(e)}")
            return None

def create_openai_client():
    return OpenAIClient()

def get_chatbot_response(client, user_input):
    context = """
    You are a friendly and knowledgeable sales assistant for a high-end home decor store specializing in lamps, curtains, and curtain drivers. Your name is Lumi.
    You're passionate about interior design and home decoration. Your goal is to help customers find the perfect lamps, curtains, and curtain drivers for their space.
    Respond in a conversational, warm manner. Use phrases a human sales assistant might use, like "I'd be happy to help with that" or "That's a great question!".
    If you don't have specific information about a product, you can say something like "I don't have all the details on hand, but I'd be happy to find out for you."
    Encourage customers to ask about lamp and curtain styles, room decoration tips, or current trends in interior design.
    Remember to occasionally ask if they need help with anything else or if they have any other questions about our products.
    When discussing lamps, you can mention aspects like light temperature, brightness, and energy efficiency.
    For curtains, you can discuss fabric types, patterns, light-blocking properties, and how they can complement room decor.
    For curtain drivers, explain their benefits such as convenience, smart home integration, and energy efficiency. Mention that they can be controlled via smartphone apps or voice assistants.
    """
    
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": user_input}
    ]
    
    response = client.chat_completion(messages)
    if response is None:
        return "I apologize, but I'm having trouble accessing my knowledge base at the moment. Let me provide you with some general information about our products. We specialize in high-quality lamps, curtains, and curtain drivers. Is there a specific category you're interested in?"
    return response
