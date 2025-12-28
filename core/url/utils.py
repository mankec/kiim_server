from urllib.parse import urlencode

def build_url_with_query(url, query: dict):
    return f"{url}?{urlencode(query)}"
