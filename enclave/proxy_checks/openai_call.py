def execute() -> (bool, str):
    try:
        import settings
        import requests

        URL = "https://api.openai.com/v1/chat/completions"
        HEADERS = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + settings.OPEN_AI_API_KEY,
        }
        DATA = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You a simple greeter"
                },
                {
                    "role": "user",
                    "content": "Greet me"
                }
            ]
        }
        result = requests.post(URL, headers=HEADERS, json=DATA)
        if not result.status_code == 200:
            return False, f"Status code from API: {result.status_code}"
        data = result.json()
        print("result:", data)
        return True, ""
    except Exception as exc:
        return False, str(exc)
