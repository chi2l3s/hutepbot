from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_setting_update_body import PostPanelSettingUpdateBody
from ...models.post_panel_setting_update_response_200 import PostPanelSettingUpdateResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelSettingUpdateBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/setting/update",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelSettingUpdateResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelSettingUpdateResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelSettingUpdateResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingUpdateBody,
) -> Response[PostPanelSettingUpdateResponse200]:
    """Persist every setting at once. The body mirrors the shape returned by /all. Invalid values (bad
    ports, missing cert pairs, etc.) are rejected before write.

    Args:
        body (PostPanelSettingUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelSettingUpdateResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingUpdateBody,
) -> PostPanelSettingUpdateResponse200 | None:
    """Persist every setting at once. The body mirrors the shape returned by /all. Invalid values (bad
    ports, missing cert pairs, etc.) are rejected before write.

    Args:
        body (PostPanelSettingUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelSettingUpdateResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingUpdateBody,
) -> Response[PostPanelSettingUpdateResponse200]:
    """Persist every setting at once. The body mirrors the shape returned by /all. Invalid values (bad
    ports, missing cert pairs, etc.) are rejected before write.

    Args:
        body (PostPanelSettingUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelSettingUpdateResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingUpdateBody,
) -> PostPanelSettingUpdateResponse200 | None:
    """Persist every setting at once. The body mirrors the shape returned by /all. Invalid values (bad
    ports, missing cert pairs, etc.) are rejected before write.

    Args:
        body (PostPanelSettingUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelSettingUpdateResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
