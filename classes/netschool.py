from typing import Self, Coroutine
from hashlib import md5
import aiohttp


class NetSchoolApi:
    __instance = None
    
    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        
        return cls.__instance
    
    def __init__(self, url: str, school: str, login: str, password: str) -> None:
        self.url = url
        self.school = school
        self.__login = login
        self.__password = password
        self.headers = {}
    
    async def login(self) -> dict:
        self._session = aiohttp.ClientSession()
        await self._school_id()
        
        req = await self._session.post(f'{self.url}/webapi/auth/getdata')
        
        data: dict = await self._config(await req.json())
        response_login = await self._session.post(f'{self.url}/webapi/login', data=data)
    
        result = await response_login.json()
            
        if 'at' not in result:
            self.__class__.__instance = None
            return {'status': False, 'messag': 'Ошибка входа. Проверьте логин и пароль.'}
        
        await self._make_attrs(result)
        # self.logout()
        return {'status': True, 'messag': 'Вход прошёл успешно'}
        
    async def _school_id(self) -> int:
        schools = await self._session.get(f'{self.url}/webapi/schools/search')
        
        for i in await schools.json():
            if self.school == i['shortName']:
                self.school_id = i['id']
                break
    
    async def make_query_parametrs(self, url: str, **kwargs) -> str:
        params = [f'{key}={value}' for key, value in kwargs.items()]
        params_part = '&'.join(params)
        
        return f'{url}?{params_part}'

    async def _config(self, req_response_dict: dict) -> dict:
        login_meta: dict = req_response_dict
        
        salt: str = login_meta.pop('salt')
        encoded_password: str = md5(self.__password.encode('windows-1251')).hexdigest().encode()

        pw2: str = md5(salt.encode() + encoded_password).hexdigest()
        pw: str = pw2[: len(self.__password)]
        
        data = {
            'LoginType': 1,
            'UN': self.__login,
            'scid': self.school_id,
            'PW': pw,
            'pw2': pw2,
            **login_meta
        }
        return data

    async def _config_mark(self, **kwargs) -> dict:
        data: dict = {
            'selectedData': [
                {'filterId': 'SID', 'filterText': self.name_surname, 'filterValue': self.student_id},
                {'filterId': 'PCLID_IUP', 'filterText': kwargs['class_name'], 'filterValue': kwargs['class_id']},
                {'filterId': 'SGID', 'filterText': kwargs['subject'], 'filterValue': kwargs['subject_id']},
                {'filterId': 'TERMID', 'filterText': '1 четверть', 'filterValue': '188190'},
                {'filterId': 'period', 'filterText': '01.09.2024 - 04.11.2024', 'filterValue': '2024-09-01T00:00:00.000Z - 2024-11-04T00:00:00.000Z'},
            ]
        }
        return data
    
    async def _make_attrs(self, result: dict) -> Coroutine:
        account_info = result['accountInfo']
        self.__at: str = result['at']
        self.student_id: int = account_info['user']['id']
        self.name_surname = account_info['user']['name']
        self.headers['At'] = self.__at
        
        request_response = await self._session.get(f'{self.url}/webapi/context', headers=self.headers)
        
        resp_json = await request_response.json()
        self.schoolYearId = resp_json['schoolYearId']
    
    async def logout(self) -> Coroutine:
        await self._session.post(f'{self.url}/webapi/auth/logout', headers=self.headers)
        await self._session.close()
    
    @classmethod
    def instance(cls) -> bool:
        return bool(cls.__instance)