import requests
from abc import ABC, abstractmethod


class AbstractJobAPI(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_term):
        pass


class HeadHunterAPI(AbstractJobAPI):
    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")

    def get_vacancies(self, search_term):
        items = []
        for i in range(5):
            response = requests.get(self.base_url,
                                    params={'text': search_term, 'per_page': 10, 'page': i, 'only_with_salary': True})
            if response.status_code == 200:
                vacancies = response.json().get('items', [])
                for vacancy in vacancies:
                    if vacancy.get('salary').get('currency') == "RUR":
                        items.append(vacancy)
            else:
                break
        return items


class SuperJobAPI(AbstractJobAPI):
    def __init__(self, secret_key):
        super().__init__("https://api.superjob.ru/2.0/vacancies/")
        self.headers = {'X-Api-App-Id': secret_key}

    def get_vacancies(self, search_term):
        items = []
        seen_vacancies = set()
        for i in range(5):
            response = requests.get(self.base_url,
                                    headers=self.headers,
                                    params={'keyword': search_term, 'no_agreement': 1, 'count': 10, 'page': i})
            if response.status_code == 200:
                vacancies = response.json().get('objects', [])
                for vacancy in vacancies:
                    if vacancy['profession'] not in seen_vacancies and vacancy['currency'] == "rub":
                        items.append(vacancy)
                        seen_vacancies.add(vacancy['profession'])
            else:
                break
        return items
