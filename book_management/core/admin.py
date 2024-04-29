from database import base

from starlette_admin.contrib.sqla import Admin
from starlette_admin.views import CustomView
from book_management.core import providers
from apps.books.admin.admin import book_transcation_view,book_view
from apps.users.admin.admin import user_view

admin = Admin(
    engine=base.engine,
    title='Admin',
    base_url="/admin",

    logo_url="https://www.svgrepo.com/show/293881/open-book-book.svg",
    login_logo_url="https://www.svgrepo.com/show/293881/open-book-book.svg",

    index_view=CustomView(label="Home", icon="fa fa-home",),
    auth_provider=providers.AdminUsernameAndPasswordProvider()
)

admin.add_view(user_view)
admin.add_view(book_view)
admin.add_view(book_transcation_view)

