import asyncio
import aiofiles
from aiohttp import ClientSession


async def schools_in_region(url: str, user_id: int):
    async with ClientSession() as session:
        req = await session.get(f'{url}/webapi/schools/search')
        schools = await req.json()
    
    async with aiofiles.open(f'{user_id}.txt', 'a', encoding='utf-8') as f:
        for school in schools:    
            await f.write(school['shortName'] + '\n')
    
    return schools