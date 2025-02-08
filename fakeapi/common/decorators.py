from functools import wraps
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar
from typing import Union

from fastapi import Request

from fakeapi.common import enums

F = TypeVar("F", bound=Callable[..., Awaitable[list[Any]]])


def sort(ordering_fields: set[str]) -> Callable[[F], F]:
    def decorator(func: Callable) -> F:
        @wraps(func)
        async def wrapper(
            request: Request,
            *args,
            **kwargs,
        ):
            data_list = await func(request, *args, **kwargs)

            if sort_by := request.query_params.get(enums.QueryParam.SORT_BY):
                reverse = sort_by.startswith("-")
                field = sort_by.lstrip("-")
                if field in ordering_fields:
                    try:
                        data_list = sorted(data_list, key=lambda x: getattr(x, field, None), reverse=reverse)
                    except TypeError:
                        pass

            return data_list

        return wrapper

    return decorator


def filter(filtering_fields: set[str]) -> Callable[[F], F]:
    def decorator(func: Callable) -> F:
        @wraps(func)
        async def wrapper(
            request: Request,
            *args,
            **kwargs,
        ):
            data_list = await func(request, *args, **kwargs)

            query_params = request.query_params

            for field in filtering_fields:
                if field in query_params:
                    filter_value = query_params.get(field)
                    # Currently, this only supports exact match filtering.
                    data_list = [
                        item for item in data_list if str(getattr(item, field, "")).lower() == filter_value.lower()
                    ]

            return data_list

        return wrapper

    return decorator


def paginate(default_page_size: int = 30, max_page_size: int = 100) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> dict[str, Union[int, None, list[Any]]]:
            data_list = await func(request, *args, **kwargs)

            page = int(request.query_params.get(enums.QueryParam.PAGE.value, 1))
            page_size = int(request.query_params.get(enums.QueryParam.PAGE_SIZE.value, default_page_size))
            page_size = min(page_size, max_page_size)

            total_items = len(data_list)
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_results = data_list[start_index:end_index]

            return {
                "count": total_items,
                "next": page + 1 if end_index < total_items else None,
                "previous": page - 1 if page > 1 else None,
                "results": paginated_results,
            }

        return wrapper

    return decorator
