import requests

# Define your Interakt API endpoint and authentication
base_url = 'https://api.interakt.ai'
api_key = 'your_api_key'
headers = {'Authorization': f'Bearer {api_key}'}

# Create a conversation with the Interakt bot
def start_conversation():
    endpoint = '/v1/conversations/start'
    payload = {
        'bot_id': 'your_bot_id',
        'user_id': 'user123',
        'message': 'Hello, chatbot!'
    }
    response = requests.post(base_url + endpoint, json=payload, headers=headers)
    return response.json()

# Send a message to the chatbot
def send_message(conversation_id, message):
    endpoint = '/v1/conversations/send'
    payload = {
        'conversation_id': conversation_id,
        'message': message
    }
    response = requests.post(base_url + endpoint, json=payload, headers=headers)
    return response.json()

# Example usage
conversation = start_conversation()
conversation_id = conversation['conversation_id']
response = send_message(conversation_id, 'How can I help you?')
print(response)
