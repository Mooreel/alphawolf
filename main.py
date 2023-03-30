import ssl
import openai
import wolframalpha
import requests
import os

CHATGPT_API_KEY = os.environ["CHATGPT_API_KEY"]
WOLFRAMALPHA_APP_ID = os.environ["WOLFRAMALPHA_APP_ID"]

openai.api_key = CHATGPT_API_KEY
chatgpt_url = "https://api.openai.com/v1/chat/completions"

wolfram_client = wolframalpha.Client(WOLFRAMALPHA_APP_ID)
MAX_TOKENS = 200


def ask_chatgpt(prompt):
    data = {
        "model": "gpt-4", #"gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Whenever you cannot answer a question very confidently and if it would be helpful to have real time knowledge, respond starting with 'solve: ' and the a consise version of the original prompt. Here is the question: {prompt}"},
        ],
        "max_tokens": MAX_TOKENS,
    }

    response = requests.post(chatgpt_url, headers={"Authorization": f"Bearer {openai.api_key}"}, json=data)
    response_json = response.json()

    if 'choices' in response_json:
        return response_json["choices"][0]["message"]["content"].strip()
    else:
        print(f"Error with ChatGPT API: {response_json}")
        return "Error: Couldn't process your query."


def ask_wolframalpha(query):
    print("Asking WolframAlpha...")
    ssl._create_default_https_context = ssl._create_unverified_context

    result = wolfram_client.query(query)
    try:
        answer = next(result.results).text
    except StopIteration:
        answer = "I couldn't find an answer to your query."
    return answer


def calculate(query):
    chatgpt_result = ask_chatgpt(query)
    if "calculate" in chatgpt_result.lower() or "solve" in chatgpt_result.lower():
        return ask_wolframalpha(query)
    return chatgpt_result


if __name__ == "__main__":
    while True:
        user_input = input("Enter your query or type 'exit' to quit: ")
        if user_input.lower() == "exit":
            break
        result = calculate(user_input)
        print(f"Result: {result}")
