import json
import requests

from functools import wraps


def cached(func):
    """Simple Cache method decorator to better handle data fetched over proxy API"""
    func.cache = {}

    @wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result

    return wrapper


@cached
def fetch_author(book_id):
    """Fetching Author name from AuthorAPI Microservice """
    try:
        url = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding"
        headers = {"content-type": "application/json"}
        data = json.dumps({"book_id": int(book_id)})
        response = requests.post(url, headers=headers, data=data,)
        return response.json().get("author")
    except Exception as e:
        print(e)
        return None
