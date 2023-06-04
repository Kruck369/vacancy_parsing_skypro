import json
from src.vacancy import Vacancy


class VacancyManager:
    def __init__(self, filename):
        self.vacancies = []
        self.filename = filename

    def add_vacancy(self, vacancy):
        if not isinstance(vacancy, Vacancy):
            raise TypeError("Вакансия должна быть экземпляром класса Vacancy")
        self.vacancies.append(vacancy)
        self.save_to_file()

    def get_vacancies(self):
        return self.vacancies

    def get_vacancies_by_salary(self):
        return sorted(self.vacancies, key=lambda v: (v.salary['min'] or 0, v.salary['max'] or 0), reverse=True)

    def delete_vacancy(self, vacancy):
        if vacancy in self.vacancies:
            self.vacancies.remove(vacancy)
            self.save_to_file()

    def save_to_file(self):
        with open(self.filename, "w") as f:
            json.dump([vars(vacancy) for vacancy in self.vacancies], f, ensure_ascii=False, indent=4)
            