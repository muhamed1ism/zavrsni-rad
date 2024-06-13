import requests
from flask import request, abort


def api_request(api, endpoint, entity_id):
    url = f"http://{api}/{endpoint}" if entity_id == '' else f"http://{api}/{endpoint}/{entity_id}"
    response = requests.get(url, headers={'Authorization': request.headers['Authorization']})
    if response:
        return response.json()
    elif ValueError:
        abort(404, description='Resource not found.')
