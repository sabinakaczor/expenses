import requests
import json
from config import Config

class ApiConnector:

    def __init__(self):
        config = Config()
        self.BASE_URI = config.get('BASE_URI')
        self.USERNAME = config.get('USERNAME')
        self.PASSWORD = config.get('PASSWORD')
        self.MY_NAME = config.get('MY_NAME')

    def get(self, path, query = {}):
        r = requests.get(self.BASE_URI + path, params = query, headers = {'Content-Type': 'application/json'}, auth = requests.auth.HTTPBasicAuth(self.USERNAME, self.PASSWORD))
        return (r.status_code, r.text)

    def post(self, path, data):
        r = requests.post(self.BASE_URI + path, json = data, headers = {'Content-Type': 'application/json'}, auth = requests.auth.HTTPBasicAuth(self.USERNAME, self.PASSWORD))
        print(r.status_code, r.text)

    def delete(self, path, query = {}):
        r = requests.delete(self.BASE_URI + path, params = query, headers = {'Content-Type': 'application/json'}, auth = requests.auth.HTTPBasicAuth(self.USERNAME, self.PASSWORD))
        print(r.status_code, r.text)

    def add_expense(self, data):
        print('Adding the expense', data)
        self.post('expenses', {'expense': data})

    def get_expenses(self):
        print('Getting the expenses list')
        ret = self.get('expenses')
        if ret[0] == 200:
            data = json.loads(ret[1])
            expenses = sorted(data['data'], key=lambda item: item['time'])
            for expense in expenses:
                if expense['name'] == self.MY_NAME:
                    print('{0:10} {1:>20} {2:>10} {3:>10}'.format(
                        expense['name'],
                        expense['purpose'],
                        expense['amount'],
                        expense['time']              
                    ))

    def get_expense(self, expense_id):
        print('Getting the expense', expense_id)
        print(self.get('expenses/{0}'.format(expense_id)))

    def delete_expense(self, expense_id):
        print('Deleting the expense', expense_id)
        self.delete('expenses/{0}'.format(expense_id))