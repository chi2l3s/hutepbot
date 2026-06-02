from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_setting_api_tokens_set_enabled_id_body import PostPanelSettingApiTokensSetEnabledIdBody
from ...models.post_panel_setting_api_tokens_set_enabled_id_response_200 import (
    PostPanelSettingApiTokensSetEnabledIdResponse200,
)
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: PostPanelSettingApiTokensSetEnabledIdBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/setting/apiTokens/setEnabled/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelSettingApiTokensSetEnabledIdResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelSettingApiTokensSetEnabledIdResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelSettingApiTokensSetEnabledIdResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingApiTokensSetEnabledIdBody,
) -> Response[PostPanelSettingApiTokensSetEnabledIdResponse200]:
    """Toggle a token enabled/disabled without deleting it. Disabled tokens are rejected by checkAPIAuth on
    the next request.

    Args:
        id (int):
        body (PostPanelSettingApiTokensSetEnabledIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelSettingApiTokensSetEnabledIdResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingApiTokensSetEnabledIdBody,
) -> PostPanelSettingApiTokensSetEnabledIdResponse200 | None:
    """Toggle a token enabled/disabled without deleting it. Disabled tokens are rejected by checkAPIAuth on
    the next request.

    Args:
        id (int):
        body (PostPanelSettingApiTokensSetEnabledIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelSettingApiTokensSetEnabledIdResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingApiTokensSetEnabledIdBody,
) -> Response[PostPanelSettingApiTokensSetEnabledIdResponse200]:
    """Toggle a token enabled/disabled without deleting it. Disabled tokens are rejected by checkAPIAuth on
    the next request.

    Args:
        id (int):
        body (PostPanelSettingApiTokensSetEnabledIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelSettingApiTokensSetEnabledIdResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelSettingApiTokensSetEnabledIdBody,
) -> PostPanelSettingApiTokensSetEnabledIdResponse200 | None:
    """Toggle a token enabled/disabled without deleting it. Disabled tokens are rejected by checkAPIAuth on
    the next request.

    Args:
        id (int):
        body (PostPanelSettingApiTokensSetEnabledIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelSettingApiTokensSetEnabledIdResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
