from __future__ import annotations

import socket
from typing import Union

from fastapi import Header, Request
from pydantic import BaseModel


def get_request_extra_data(
    request: Request,
    correlation_id: str = Header(None, alias="x-correlation_id"),
    root_action: str = Header(None, alias="x-root_action"),
    user_id: str = Header(None, alias="x-user_id"),
):
    return {
        "correlation_id": correlation_id,
        "root_action": root_action,
        "user_id": user_id,
        "trace_id": request.state.trace_id,
        "current_action": str(request.url),
    }


class PropertyBaseModel(BaseModel):
    """
    Workaround for serializing properties with pydantic until
    https://github.com/samuelcolvin/pydantic/issues/935
    is solved
    """

    @classmethod
    def get_properties(cls):
        return [
            prop
            for prop in dir(cls)
            if isinstance(getattr(cls, prop), property)
            and prop not in ("__values__", "fields")
        ]

    def dict(
        self,
        *,
        include: Union["AbstractSetIntStr", "MappingIntStrAny"] = None,
        exclude: Union["AbstractSetIntStr", "MappingIntStrAny"] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs


def get_ip_6(host, port=80):
    alladdr = socket.getaddrinfo(host, port)
    ip6 = filter(lambda x: x[0] == socket.AF_INET6, alladdr)  # means its ip6
    try:
        return str(list(ip6)[0][4][0])
    except IndexError:
        return None
