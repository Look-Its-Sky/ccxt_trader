import requests
import os

def send(msg: str):
    requests.post(f'https://{os.environ["NTFY_SERVER"]}', data=msg)
