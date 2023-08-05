"""
Type annotations for sso service type definitions.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_sso/type_defs.html)

Usage::

    ```python
    from types_aiobotocore_sso.type_defs import AccountInfoTypeDef

    data: AccountInfoTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountInfoTypeDef",
    "GetRoleCredentialsRequestRequestTypeDef",
    "GetRoleCredentialsResponseTypeDef",
    "ListAccountRolesRequestRequestTypeDef",
    "ListAccountRolesResponseTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "ListAccountsResponseTypeDef",
    "LogoutRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RoleCredentialsTypeDef",
    "RoleInfoTypeDef",
)

AccountInfoTypeDef = TypedDict(
    "AccountInfoTypeDef",
    {
        "accountId": str,
        "accountName": str,
        "emailAddress": str,
    },
    total=False,
)

GetRoleCredentialsRequestRequestTypeDef = TypedDict(
    "GetRoleCredentialsRequestRequestTypeDef",
    {
        "roleName": str,
        "accountId": str,
        "accessToken": str,
    },
)

GetRoleCredentialsResponseTypeDef = TypedDict(
    "GetRoleCredentialsResponseTypeDef",
    {
        "roleCredentials": "RoleCredentialsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListAccountRolesRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountRolesRequestRequestTypeDef",
    {
        "accessToken": str,
        "accountId": str,
    },
)
_OptionalListAccountRolesRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountRolesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAccountRolesRequestRequestTypeDef(
    _RequiredListAccountRolesRequestRequestTypeDef, _OptionalListAccountRolesRequestRequestTypeDef
):
    pass


ListAccountRolesResponseTypeDef = TypedDict(
    "ListAccountRolesResponseTypeDef",
    {
        "nextToken": str,
        "roleList": List["RoleInfoTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListAccountsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountsRequestRequestTypeDef",
    {
        "accessToken": str,
    },
)
_OptionalListAccountsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAccountsRequestRequestTypeDef(
    _RequiredListAccountsRequestRequestTypeDef, _OptionalListAccountsRequestRequestTypeDef
):
    pass


ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef",
    {
        "nextToken": str,
        "accountList": List["AccountInfoTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LogoutRequestRequestTypeDef = TypedDict(
    "LogoutRequestRequestTypeDef",
    {
        "accessToken": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

RoleCredentialsTypeDef = TypedDict(
    "RoleCredentialsTypeDef",
    {
        "accessKeyId": str,
        "secretAccessKey": str,
        "sessionToken": str,
        "expiration": int,
    },
    total=False,
)

RoleInfoTypeDef = TypedDict(
    "RoleInfoTypeDef",
    {
        "roleName": str,
        "accountId": str,
    },
    total=False,
)
