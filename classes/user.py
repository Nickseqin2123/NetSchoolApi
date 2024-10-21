from datetime import date, timedelta, datetime
from .netschool import NetSchoolApi


class User(NetSchoolApi):
    
    def __init__(self, url: str = None, school: str = None, login: str = None, password: str = None):
        if (hasattr(self, 'url') and hasattr(self, 'school') and hasattr(self, '_NetSchoolApi__login') and hasattr(self, '_NetSchoolApi__password')) is False:
            if all((url, school, password, login)):
                super().__init__(url, school, login, password)
            else:
                raise TypeError
    
    def currentweek_correct(self, start: str = None) -> tuple[str, str]:
        """
        
        Args:
            start (str, 'Y-M-D'): Год-Месяц-День.
        Returns:
            tuple: Кортеж с датами в формате (Начало недели, Конец недели)
        """
        if not start:
            monday = date.today() - timedelta(days=date.today().weekday())
            start = monday
        else:
            dt = datetime.strptime(start, "%Y-%m-%d")
            
            if dt.weekday() == 0 and dt.year == datetime.now().year:
                start = date.fromisoformat(start)
            else:
                return {'message': 'Начало недели или год не верен!', 'status': False}
        
        end = start + timedelta(days=6)

        return {'data': (start.isoformat(), end.isoformat()), 'status': True}
        
    def diary(self, start: str = None) -> dict:
        date: dict = self.currentweek_correct(start)
        
        if date['status']:
            start, end = date['data']
            
            data: dict = {
                'schoolId': self.school_id,
                'studentId': self.student_id,
                'weekEnd': end,
                'weekStart': start,
                'yearId': self.schoolYearId
            }
            url = self.make_query_parametrs('https://net-school.cap.ru/webapi/student/diary', **data)
            
            try:
                response = self._session.get(url, headers=self.headers)
                result: dict = response.json()
            except Exception:
                if self.login()['status']:
                    response = self._session.get(url, headers=self.headers)
                    result: dict = response.json()
                
            return {'message': result, 'status': True}
            
        return date
    
    # def subject_mark(self, name: str):
    #     req = self._session.get(f'{self.url}/webapi/v2/reports/studentgrades', headers=self.headers)
    #     result = req.json()['filterSources']
        
    #     result_first = result[1]
    #     subjects_num_dict = result[2]
        
    #     class_id = result_first['defaultValue']
    #     class_name = result_first['items'][0].get('title')
        
    #     for i in subjects_num_dict['items']:
    #         if i['title'] == name:
    #             subject = i['title']
    #             subject_id = i['value']
    #             break
    #     else:
    #         raise SubjectNotFound('Предмет не найден! Проверьте его название!')
        
    #     data: dict = self._config_mark(class_name=class_name, class_id=class_id, subject=subject, subject_id=subject_id)
    #     initfilters_req = self._session.post(f'{self.url}/webapi/v2/reports/studentgrades/initfilters', json=data, headers=self.headers)


# user = User('https://net-school.cap.ru/', 'МБОУ "СОШ № 30" г. Чебоксары', 'ГригорьевН29', 'NekitVip123')
# user.login()
# print(user.diary('2024-10-14'))
# user.logout()