import json

from src.vacancy import Vacancy
from src.vacancy_manager import VacancyManager
from src.api2 import HeadHunterAPI, SuperJobAPI
import os

secret_key = os.getenv('SUPER_JOB_API_KEY')


def filter_vacancies(vacancies, filter_words):
    if not filter_words:
        return vacancies

    filtered_vacancies = []
    for vacancy in vacancies:
        vacancy_info = f"{vacancy.title} {vacancy.requirements}"
        if any(word.lower() in vacancy_info.lower() for word in filter_words):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_vacancies(vacancies):
    return sorted(vacancies, key=lambda v: (v.salary['min'] or 0, v.salary['max'] or 0), reverse=True)


def get_top_vacancies(vacancies, n):
    return vacancies[:n]


def print_vacancies(vacancies):
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")


def user_interaction():
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI(secret_key)
    vacancy_manager = VacancyManager('vacancies.json')

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    hh_vacancies = hh_api.get_vacancies(search_query)
    superjob_vacancies = superjob_api.get_vacancies(search_query)

    for vac_data in hh_vacancies:
        vacancy = Vacancy.from_dict(vac_data, 'hh')
        vacancy_manager.add_vacancy(vacancy)

    for vac_data in superjob_vacancies:
        vacancy = Vacancy.from_dict(vac_data, 'sj')
        vacancy_manager.add_vacancy(vacancy)

    if not vacancy_manager.get_vacancies():
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    filtered_vacancies = filter_vacancies(vacancy_manager.get_vacancies(), filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответсвующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)

