import requests

API_KEY = "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"

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "أنت مساعد ذكي للجامعة الافتراضية السورية. إذا كان السؤال عن الجامعة فأجب بإيجاز وباللغة العربية، وإذا كان سؤالًا عامًا فأجب بشكل صحيح ومختصر."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=20
        )

        print("=" * 50)
        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)
        print("=" * 50)

        if response.status_code != 200:
            return None

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return None

    except Exception as e:
        print("=" * 50)
        print("ERROR:", e)
        print("=" * 50)
        return None
  