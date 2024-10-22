from typing import AsyncGenerator
from datetime import datetime
from other.constants import DAYS


async def assigments_parse(assigments: list) -> str:
    marks: list[dict] = []
    
    for i in assigments:
        if i.get('mark'):
            marks.append(str(i.get('mark')['mark']))
    
    return " ".join(marks) if marks else 'Не оценено'
    

async def convert_and_set_in_dict(week_days: list) -> dict[dict]:
    lessons_dct: dict = {}
    data: dict = {'main': {}}
        
    for i in range(len(week_days)):
        date_day = week_days[i]['date']

        for less in week_days[i]['lessons']:
            subject_name: str = less['subjectName']
            
            if less['assignments']:
                response: dict = await assigments_parse(less['assignments'])
                
                lessons_dct[subject_name] = response
            else:
                lessons_dct[subject_name] = 'Не оценено'
                
        data['main'].update({date_day: lessons_dct.copy()})
        lessons_dct.clear()
    
    return data
    

async def diary_print(data: dict) -> AsyncGenerator:
    for i in sorted(data['main'], key=lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").weekday()):
        day_name = DAYS[datetime.strptime(i, "%Y-%m-%dT%H:%M:%S").weekday()]
        normal = [f'{k}: {v}' for k, v in data['main'][i].items()]
        day = '\n'.join(normal)
        
        yield f'''День недели: {day_name}
{"-" * (len(day_name)+14)}
{day}\n'''