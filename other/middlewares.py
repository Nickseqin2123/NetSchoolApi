from pprint import pprint

from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class SchoolMiddlware(BaseMiddleware):
    
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        message = data['event_update']
        
        data = {'school': message.message.text, **data}
             
        result = await handler(event, data)
        return result