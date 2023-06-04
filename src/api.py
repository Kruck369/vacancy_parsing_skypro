import requests
from abc import ABC, abstractmethod


class JobPlatformAPI(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass


class HeadHunterAPI(JobPlatformAPI):
    def __init__(self, base_url='https://api.hh.ru'):
        super().__init__(base_url)

    def get_vacancies(self, search_query, **kwargs):
        url = f'{self.base_url}/vacancies'
        params = {'area': 113, 'text': search_query, **kwargs}
        response = requests.get(url, params=params,)
        return response.json()


class SuperJobAPI(JobPlatformAPI):
    def __init__(self,
                 app_secret_key='v3.r.137561840.ee036a8bfce1ea71f8ea87852dafd6ff8a01a112.fb9d098dfe8d59f45b3437a0e5cfc20dee7b3983',
                 base_url='https://api.superjob.ru/2.0'):
        super().__init__(base_url)
        self.__app_secret_key = app_secret_key

    @property
    def app_secret_key(self):
        return self.__app_secret_key

    @app_secret_key.setter
    def app_secret_key(self, app_secret_key):
        self.__app_secret_key = app_secret_key

    def get_vacancies(self, search_query, **kwargs):
        url = f"{self.base_url}/vacancies/"
        headers = {'X-Api-App-Id': self.app_secret_key}
        params = {'keyword': search_query, **kwargs}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


