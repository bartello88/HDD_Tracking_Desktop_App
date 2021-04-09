import requests
from config import TOKEN, URL

mytoken = TOKEN
url = URL

def send_to_heimdall(json_data):
    if isinstance(json_data, dict):
        response = requests.post(url,
                                 json=json_data,
                                 params={'token': mytoken}
                                 )

        response.raise_for_status()
        print(response.status_code)
        # return jsonify(response.status_code)
        return response.json(), response.status_code

