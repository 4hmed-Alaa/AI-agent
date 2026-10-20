import httpx, os

url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent'

headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': os.environ["API_KEY"]
}

payload = {
  "contents": [
    {
      "parts": [
        {
          "text": "say hello world"
        }
      ]
    }
  ]
}

response = httpx.post(url, headers=headers, json=payload, timeout=30)
response.raise_for_status()
print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
