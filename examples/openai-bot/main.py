import openai
from textbase import bot, Message
from textbase.models import OpenAI
from typing import List

# Load your OpenAI API key
OpenAI.api_key = ""

# Prompt for GPT-3.5 Turbo
# SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like.
# The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a
# pleasant chat!
# """
SYSTEM_PROMPT = """Welcome to the Mental Health Chatbot. You can ask questions or discuss topics related to mental health, emotions, and well-being. Our chatbot is here to provide support and information. Feel free to start the conversation."""


@bot()
def on_message(message_history: List[Message], state: dict = None):

    # Generate GPT-3.5 Turbo response
    user_messages = message_history[-1]
    user_message = user_messages['content'][0]['value']
    user_message_lower = user_message.lower()

    sentiment = analyze_sentiment(user_message,message_history).lower()
    if sentiment=='negative':
        if any(keyword in user_message_lower for keyword in ["stress", "anxiety", "depression", "loneliness"]):
            bot_response = handle_mental_health_issue(user_message_lower)
        elif "therapy" in user_message_lower or "counseling" in user_message_lower:
            bot_response = provide_therapy_info()
        elif "journal" in user_message_lower:
            bot_response = suggest_journaling()
        else:
            bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history, # Assuming history is the list of user messages
            model="gpt-3.5-turbo",
        )
    else:
        # For other topics or general conversation, use GPT-3.5 Turbo
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history, # Assuming history is the list of user messages
            model="gpt-3.5-turbo",
        )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }

def analyze_sentiment(input,text):
    # You can use GPT-3.5 Turbo to analyze sentiment
    response = OpenAI.generate(
        system_prompt=f"Analyze the sentiment of the following text: \"{input}\" Return response in positive for 'positive', negative for 'negative' and neutral for 'neutral' only in one word.",
        model="gpt-3.5-turbo",
        max_tokens=1,  # Limit the response to a single token (e.g., "positive", "negative", "neutral")
        message_history=text
    )
    return response

def handle_mental_health_issue(user_message_lower):
    if "stress" in user_message_lower:
        bot_response = "I'm here to help you with managing stress. It's important to find healthy ways to cope with stress. Would you like some tips?"
    elif "anxiety" in user_message_lower:
        bot_response = "I understand that anxiety can be challenging. Let's talk about it. What specific concerns or symptoms are you experiencing?"
    elif "depression" in user_message_lower:
        bot_response = "I'm here to listen and offer support. Dealing with depression can be tough. How can I assist you today?"
    elif "loneliness" in user_message_lower:
        bot_response = "I'm here to keep you company and provide support. Loneliness can affect us all. How can I make you feel less alone?"
    return bot_response

def provide_therapy_info():
    bot_response = "Therapy can be a valuable resource. If you have questions about therapy or need help finding a therapist, I can provide information."
    return bot_response

def suggest_journaling():
    bot_response = "Journaling can be a great way to express your thoughts and feelings. Try writing about your day or your emotions. It can be very therapeutic."
    return bot_response

