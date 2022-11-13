import requests

api_url = 'https://api.api-ninjas.com/v1/cars'
api_key = "sSP+krjLeIP0xGsHhLzv1Q==gXBSwzAkgbpnXqMJ"


def get_from_model(model):
    url = api_url + '?model=' + model
    response = requests.get(url,
                            headers={'X-Api-Key': api_key})
    if response.ok:
        return response.text
    else:
        return response
