import requests


def print_response():
    response = requests.get("http://api.open-notify.org/astros.json")
    print(f'response to have {response}')
    return response


def print_custom_response(address):
    response = requests.get(address)
    print(f'custom response to have {response}')
    return response
