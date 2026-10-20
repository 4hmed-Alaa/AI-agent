import httpx, os

url = 'https://generativelanguage.googleapis.com/v1beta/interactions'

headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': os.environ["API_KEY"]
}


history = []

def append_user_request(history, new_question):
    history.append({ "type": "user_input", "content": [{ "type": "text", "text": new_question }] })
    return


while True:
    try:
        question = input("ask anything? \n")
    except (EOFError, KeyboardInterrupt):
        print("Bye\n")
        break

    append_user_request(history, question)

    payload = {
        "store": False,
        "model": "gemini-3.5-flash-lite",
        "input": history
    }

    response = httpx.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    history.extend(response.json()["steps"])

    print(response.json()["steps"][1]["content"][-1]["text"] + "\n")
