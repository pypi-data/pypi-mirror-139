import requests

def get():
    req = requests.get("https://api.ipify.org/?format=text")
    
    ip = req.text

    return ip