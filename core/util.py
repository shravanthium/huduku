import json
import requests


def fetch_author(book_id):
    try:
        url = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding"
        response = requests.post(
            url,
            headers={"content-type": "application/json"},
            data=json.dumps({"book_id": int(book_id)}),
        )
        return response.json().get("author")
    except Exception as e:
        print(e)
        return None
