from pprint import pprint
from datetime import date, timedelta, datetime
from classes.netschool import NetSchoolApi
from errors import SubjectNotFound


class User(NetSchoolApi):
    
    def __init__(self, url, school, login, password):
        super().__init__(url, school, login, password)
    
    def currentweek_correct(self, start: str = None, end: str = None) -> tuple[str, str]:
        """
        
        Args:
            start (str, 'Y-M-D'): Год-Месяц-День.
            end (str, 'Y-M-D'): Год-Месяц-День.

        Returns:
            tuple: Кортеж с датами в формате (Начало недели, Конец недели)
        """
        if not start:
            monday = date.today() - timedelta(days=date.today().weekday())
            start = monday
        else:
            if datetime.strptime(start, "%Y-%m-%d").weekday() == 0:
                start = date.fromisoformat(start)
            else:
                return 'Начало недели не верно!', 0
        
        if not end:
            end = start + timedelta(days=6)
        else:
            if datetime.strptime(end, "%Y-%m-%d").weekday() == 6:
                end = date.fromisoformat(end)
            else:
                return 'Конец недели не верен!', 0
    
        return start.isoformat(), end.isoformat()
        
    def diary(self, start: str = None, end: str = None) -> dict:
        date = self.currentweek_correct(start, end)
        
        if all(date):
            start, end = date
            
            data: dict = {
                'schoolId': self.school_id,
                'studentId': self.student_id,
                'weekEnd': end,
                'weekStart': start,
                'yearId': self.schoolYearId
            }
            url = self.make_query_parametrs('https://net-school.cap.ru/webapi/student/diary', **data)
            
            response = self._session.get(url, headers=self.headers)
            result: dict = response.json()
            
            return result
            
        return date[0]
    
    def subject_mark(self, name: str):
        req = self._session.get(f'{self.url}/webapi/v2/reports/studentgrades', headers=self.headers)
        result = req.json()['filterSources']
        
        result_first = result[1]
        subjects_num_dict = result[2]
        
        class_id = result_first['defaultValue']
        class_name = result_first['items'][0].get('title')
        
        for i in subjects_num_dict['items']:
            if i['title'] == name:
                subject = i['title']
                subject_id = i['value']
                break
        else:
            raise SubjectNotFound('Предмет не найден! Проверьте его название!')
        
        data: dict = self._config_mark(class_name=class_name, class_id=class_id, subject=subject, subject_id=subject_id)
        initfilters_req = self._session.post(f'{self.url}/webapi/v2/reports/studentgrades/initfilters', json=data, headers=self.headers)
        

user = User('https://net-school.cap.ru', 'МБОУ "СОШ № 30" г. Чебоксары', 'ГригорьевН29', 'NekitVip123')
user.login()
user.subject_mark('Алгебра')
user.logout()