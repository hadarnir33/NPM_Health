from fastapi import Response
import requests
import json


def send_request_to_healthy(packages: dict, response: Response) -> Response:
    url = f'http://127.0.0.1:9000/packages'
    healthy_response = requests.post(url, json=packages)
    response.body = healthy_response.content
    response.status_code = healthy_response.status_code
    return response
