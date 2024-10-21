from typing import Generator
from datetime import datetime
from other.constants import DAYS
from classes.user import User


def assigments_parse(assigments: list):
    marks: list[dict] = []
    
    for i in assigments:
        if i.get('mark'):
            marks.append(str(i.get('mark')['mark']))
    
    return " ".join(marks) if marks else 'Не оценено'
    

def convert_and_set_in_dict(week_days: list):
    lessons_dct: dict = {}
    data: dict = {'main': {}}
        
    for i in range(len(week_days)):
        date_day = week_days[i]['date']

        for less in week_days[i]['lessons']:
            subject_name: str = less['subjectName']
            
            if less['assignments']:
                response: dict = assigments_parse(less['assignments'])
                
                lessons_dct[subject_name] = response
            else:
                lessons_dct[subject_name] = 'Не оценено'
                
        data['main'].update({date_day: lessons_dct.copy()})
        lessons_dct.clear()
    
    return data
    

def diary_print(data: dict) -> Generator:
    for i in sorted(data['main'], key=lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").weekday()):
        day_name = DAYS[datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").weekday()]
        normal = [f'{k}: {v}' for k, v in data['main'][i].items()]
        day = '\n'.join(normal)
        
        yield f'''День недели: {day_name}
{"-" * (len(day_name)+14)}
{day}\n'''


# def main():
#     url = input('Введите url сайта: ')
#     school = input('Введите свою школу: ')
#     login = input('Введите свой логин: ')
#     password = input('Введите свой пароль: ')
#     user = User(url, school, login, password)
    
#     user.login()
#     src: dict = user.diary('2024-10-14')
#     user.logout()
#     data: dict = convert_and_set_in_dict(src['weekDays'])
    
#     for i in diary_print(data):
#         print(i)


# main()