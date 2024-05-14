from starlette_admin.contrib.sqla import Admin
from starlette_admin.views import CustomView
from book_management.core import providers
from apps.books.admin.admin import book_transaction_view, book_view
from apps.users.admin.admin import user_view
from book_management.core.config import settings
from database.base import async_sessionmanager

admin = Admin(
    engine=async_sessionmanager.engine,
    title='Admin',
    base_url="/admin",

    logo_url=settings.LOGO_URL,
    login_logo_url=settings.LOGIN_LOGO_URL,

    index_view=CustomView(label="Home", icon="fa fa-home", ),
    auth_provider=providers.AdminUsernameAndPasswordProvider()
)

admin.add_view(user_view)
admin.add_view(book_view)
admin.add_view(book_transaction_view)
