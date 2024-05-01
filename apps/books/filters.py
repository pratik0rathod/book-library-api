from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from apps.books import models


class FilterModelBook(Filter):
    title__like: Optional[str] = None
    author__like: Optional[str] = None
    ratings__gte: Optional[float] = None
    ratings__lte: Optional[float] = None
    is_available: Optional[bool] = None

    class Constants(Filter.Constants):
        model = models.Books
        search_field_name = "search"
        search_model_fields = ['title', 'author', 'ratings']
