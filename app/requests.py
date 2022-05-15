import requests
from urllib import response
from .models import Quote
import urllib.request,json

url = "http://quotes.stormconsultancy.co.uk/random.json"

base_url = url
def get_quote():
    """
    Function to consume http request and return a Quote class instance
    """
    response = requests.get(url).json()

    random_quote = Quote(response.get("author"), response.get("quote"))
    return random_quote

    # random_quote = Quote(response.get("author"), response.get("quote", response.get('permalink')))
    # return random_quote