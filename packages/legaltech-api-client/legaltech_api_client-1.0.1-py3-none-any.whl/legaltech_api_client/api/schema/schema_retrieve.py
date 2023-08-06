from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.schema_retrieve_format import SchemaRetrieveFormat
from ...models.schema_retrieve_lang import SchemaRetrieveLang
from ...models.schema_retrieve_response_200 import SchemaRetrieveResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, SchemaRetrieveFormat] = UNSET,
    lang: Union[Unset, None, SchemaRetrieveLang] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/schema/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_format_: Union[Unset, None, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value if format_ else None

    params["format"] = json_format_

    json_lang: Union[Unset, None, str] = UNSET
    if not isinstance(lang, Unset):
        json_lang = lang.value if lang else None

    params["lang"] = json_lang

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[SchemaRetrieveResponse200]:
    if response.status_code == 200:
        response_200 = SchemaRetrieveResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[SchemaRetrieveResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, SchemaRetrieveFormat] = UNSET,
    lang: Union[Unset, None, SchemaRetrieveLang] = UNSET,
) -> Response[SchemaRetrieveResponse200]:
    """OpenApi3 schema for this API. Format can be selected via content negotiation.

    - YAML: application/vnd.oai.openapi
    - JSON: application/vnd.oai.openapi+json

    Args:
        format_ (Union[Unset, None, SchemaRetrieveFormat]):
        lang (Union[Unset, None, SchemaRetrieveLang]):

    Returns:
        Response[SchemaRetrieveResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        format_=format_,
        lang=lang,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, SchemaRetrieveFormat] = UNSET,
    lang: Union[Unset, None, SchemaRetrieveLang] = UNSET,
) -> Optional[SchemaRetrieveResponse200]:
    """OpenApi3 schema for this API. Format can be selected via content negotiation.

    - YAML: application/vnd.oai.openapi
    - JSON: application/vnd.oai.openapi+json

    Args:
        format_ (Union[Unset, None, SchemaRetrieveFormat]):
        lang (Union[Unset, None, SchemaRetrieveLang]):

    Returns:
        Response[SchemaRetrieveResponse200]
    """

    return sync_detailed(
        client=client,
        format_=format_,
        lang=lang,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, SchemaRetrieveFormat] = UNSET,
    lang: Union[Unset, None, SchemaRetrieveLang] = UNSET,
) -> Response[SchemaRetrieveResponse200]:
    """OpenApi3 schema for this API. Format can be selected via content negotiation.

    - YAML: application/vnd.oai.openapi
    - JSON: application/vnd.oai.openapi+json

    Args:
        format_ (Union[Unset, None, SchemaRetrieveFormat]):
        lang (Union[Unset, None, SchemaRetrieveLang]):

    Returns:
        Response[SchemaRetrieveResponse200]
    """

    kwargs = _get_kwargs(
        client=client,
        format_=format_,
        lang=lang,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, None, SchemaRetrieveFormat] = UNSET,
    lang: Union[Unset, None, SchemaRetrieveLang] = UNSET,
) -> Optional[SchemaRetrieveResponse200]:
    """OpenApi3 schema for this API. Format can be selected via content negotiation.

    - YAML: application/vnd.oai.openapi
    - JSON: application/vnd.oai.openapi+json

    Args:
        format_ (Union[Unset, None, SchemaRetrieveFormat]):
        lang (Union[Unset, None, SchemaRetrieveLang]):

    Returns:
        Response[SchemaRetrieveResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            format_=format_,
            lang=lang,
        )
    ).parsed
