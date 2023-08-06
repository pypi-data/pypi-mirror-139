import requests
import fake_useragent
import json


class EasyLiker:
    url = 'https://easyliker.ru/api'
    user = fake_useragent.UserAgent().random
    headers = {
        'user-agent': user,
        "Content-type": "application/json"
    }

    def __init__(self, token: str):
        self.token = token

    def get_balance(self):
        data = {
            'api_token': self.token,
            'method': 'getBalance',
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def get_service_version(self):
        data = {
            'api_token': self.token,
            'method': 'getServiceVersion',
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def get_services(self):
        data = {
            'api_token': self.token,
            'method': 'getServices',
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def create_Task(self, site: str, type_of_task: str, quality: str, link: str, count: int, option: list):
        data = {
            'api_token': self.token,
            'method': 'createTask',
            'website': site,
            'type': type_of_task,
            'quality': quality,
            'link': link,
            'count': count,
            'option': option
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def get_tasks(self, id=0, count=20, offset=0):
        if id != 0:
            data = {
                'api_token': self.token,
                'method': 'getTasks',
                'id ': id,
                'count': 1
            }
        else:
            data = {
                'api_token': self.token,
                'method': 'getTasks',
                'id ': id,
                'count': count,
                'offset': offset
            }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def get_payment_methods(self):
        data = {
            'api_token': self.token,
            'method': 'getPaymentMethods',
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def create_payment(self, sum: float, payment: str):
        data = {
            'api_token': self.token,
            'method': 'createPayment',
            'sum': sum,
            'payment_system': payment
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response

    def getProfileData(self):
        data = {
            'api_token': self.token,
            'method': 'getProfileData'
        }
        data_json = json.dumps(data)
        response = requests.post(url=EasyLiker.url, headers=EasyLiker.headers, data=data_json).json()
        return response
