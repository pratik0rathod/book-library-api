from apps.users import models
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional

class FilterModelUser(Filter):
    username__like:Optional[str] = None
   
    class Constants(Filter.Constants):
        model = models.Users
        search_field_name = "search"
        search_model_fields = ['username']
