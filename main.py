import sys  # for end execution of code while error occurs

import requests  # lib for make a request to API
from prettytable import PrettyTable  # lib for make output looks nice


def get_date():  # get date from user
    user_data_input = input('Podaj datę (RRRR-MM-DD): ')
    return user_data_input


def get_currencies():  # get 4 currencies from user and store them in list
    user_currencies_list = []
    for counter in range(4):
        user_currencies_list.append(input('Podaj walutę: '))
    return user_currencies_list


class Currency:
    def __init__(self, user_currency, user_data):  # construct currency object
        self.user_currency = user_currency
        self.user_data = user_data
        self.result_storage = []

    def fetch_data(self):  # fetching data from NBP API
        api_url = f'http://api.nbp.pl/api/exchangerates/tables/a/{self.user_data}'
        try:
            resp = requests.get(api_url)
            if resp.ok:
                resp = resp.json()
                self.find_currencies(resp, self.user_currency)
            else:
                raise Exception('\n Nieprawidłowa data')
        except Exception as dateError:
            print(dateError)
            sys.exit()

    def find_currencies(self, data, currencies):  # find user's currencies and store them
        for values in data[0]['rates']:
            for i in range(4):
                if currencies[i] in values['currency']:
                    self.result_storage.append(
                        {'currency': values['currency'], 'code': values['code'].upper(), 'mid': values['mid']})

    def print_currencies(self):  # print results
        table = PrettyTable()
        table.field_names = ['Waluta', 'Kod waluty', 'Średni kurs']
        table.align = 'l'
        try:
            table.add_rows(
                [
                    [self.result_storage[0]['currency'].upper(), self.result_storage[0]['code'],
                     self.result_storage[0]['mid']],
                    [self.result_storage[1]['currency'].upper(), self.result_storage[1]['code'],
                     self.result_storage[1]['mid']],
                    [self.result_storage[2]['currency'].upper(), self.result_storage[2]['code'],
                     self.result_storage[2]['mid']],
                    [self.result_storage[3]['currency'].upper(), self.result_storage[3]['code'],
                     self.result_storage[3]['mid']],
                ]
            )
            print(table)
        except IndexError as err:  # if array is empty or len<4
            print(err)


def main():
    user_data = get_date()
    user_currencies = get_currencies()

    call_api = Currency(user_currencies, user_data)
    call_api.fetch_data()
    call_api.print_currencies()


if __name__ == '__main__':
    main()
