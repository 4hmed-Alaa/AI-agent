import httpx, os

url = 'https://generativelanguage.googleapis.com/v1beta/interactions'

headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': os.environ["API_KEY"]
}


while True:
    try:
        question = input("ask anything? \n")
    except (EOFError, KeyboardInterrupt):
        print("Bye\n")
        break

    payload = {
        "store": False,
        "model": "gemini-3.5-flash-lite",
        "input": question
    }
    response = httpx.post(url, headers=headers, json=payload, timeout=30)

    response.raise_for_status()
    print(response.json()["steps"][1]["content"][0]["text"] + "\n")

