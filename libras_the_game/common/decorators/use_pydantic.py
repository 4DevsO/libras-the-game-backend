# Python imports
from functools import wraps
from typing import Callable, Optional, Type

# Pip imports
from flask import Response, current_app, jsonify, make_response, request
from flask_pydantic import validate
from flask_pydantic.core import unsupported_media_type_response
from flask_pydantic.exceptions import JsonBodyParsingError
from pydantic import BaseModel, ValidationError


def use_pydantic(
    body: Optional[Type[BaseModel]] = None,
    query: Optional[Type[BaseModel]] = None,
    on_success_status: int = 200,
    exclude_none: bool = False,
    response_many: bool = False,
    request_body_many: bool = False,
    response_by_alias: bool = False,
    get_json_params: Optional[dict] = None,
    form: Optional[Type[BaseModel]] = None,
) -> Response:
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Parse request
            f, err = None, {}
            form_in_kwargs = func.__annotations__.get("form")
            form_model = form_in_kwargs or form
            if form_model:
                form_params = request.form
                if "__root__" in form_model.__fields__:
                    try:
                        f = form_model(__root__=form_params).__root__
                    except ValidationError as ve:
                        err["form_params"] = ve.errors()
                else:
                    try:
                        f = form_model(**form_params)
                    except TypeError:
                        content_type = request.headers.get("Content-Type", "").lower()
                        media_type = content_type.split(";")[0]
                        if media_type != "multipart/form-data":
                            return unsupported_media_type_response(content_type)
                        else:
                            raise JsonBodyParsingError
                    except ValidationError as ve:
                        err["form_params"] = ve.errors()
            request.form_params = f
            if form_in_kwargs:
                kwargs["form"] = f
            if err:
                status_code = current_app.config.get(
                    "FLASK_PYDANTIC_VALIDATION_ERROR_STATUS_CODE", 400
                )
                return make_response(jsonify({"validation_error": err}), status_code)
            form_annotation = func.__annotations__.pop("form", None)

            validate_resp = validate(
                body,
                query,
                on_success_status,
                exclude_none,
                response_many,
                request_body_many,
                response_by_alias,
                get_json_params,
            )(func)(*args, **kwargs)
            func.__annotations__["form"] = form_annotation
            return validate_resp

        return wrapper

    return decorate
