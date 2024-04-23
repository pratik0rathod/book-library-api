from database import base
from starlette_admin.contrib.sqla import Admin,ModelView
from starlette_admin.views import CustomView
from . import providers,views
from apps.users import models,schema
from apps.books import schema as bookschema
admin = Admin(
    engine=base.engine,
    title='Admin',
    base_url="/admin",

    logo_url="https://preview.tabler.io/static/logo-white.svg",
    login_logo_url="https://preview.tabler.io/static/logo.svg",

    index_view=CustomView(label="Home", icon="fa fa-home",),
    auth_provider=providers.AdminUsernameAndPasswordProvider()
)

admin.add_view(views.UserView(
    model=models.Users,
    label="Users",
    icon="fa fa-users",
    pydantic_model=schema.UserRegister,
))


admin.add_view(views.BookView(
    model=models.Books,
    label="Books",
    icon="fa fa-book",
    pydantic_model=bookschema.BooksSchema
))