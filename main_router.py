from aiogram import Router
from user.login import router as user_login_router
from user.logout import router as user_logout_router
from user.diary import router as user_diary_router
from user.support import router as user_support_router


router = Router(name=__name__)


router.include_routers(
    user_login_router,
    user_logout_router,
    user_diary_router,
    user_support_router
)