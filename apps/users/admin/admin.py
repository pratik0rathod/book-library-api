from apps.users.schema import UserRegister
from apps.users.models import Users
from apps.users.admin.view import UserView

user_view = UserView(
    model=Users,
    label="Users",
    icon="fa fa-users",
    pydantic_model=UserRegister,
)

