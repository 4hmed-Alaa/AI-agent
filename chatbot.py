import httpx, os

url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent'

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
      "contents": [
        {
          "parts": [
            {
              "text": question
            }
          ]
        }
      ]
    }

    response = httpx.post(url, headers=headers, json=payload, timeout=30)

    response.raise_for_status()
    print(response.json()["candidates"][0]["content"]["parts"][0]["text"] + "\n")

