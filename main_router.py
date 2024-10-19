from aiogram import Router
from user.login import router as user_login_router


router = Router(name=__name__)

router.include_routers(
    user_login_router
)