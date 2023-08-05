import aiohttp
from typing import Any, Dict


async def request(
    hub,
    method: str,
    url: str,
    headers: Dict[str, Any],
    base_path: str = "",
    ref: str = "",
    data: Any = None,
    json: Dict[str, Any] = None,
    **kwargs,
):
    full_url = "/".join(x for x in (url, base_path, ref) if x)
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method,
            url=full_url,
            headers=headers,
            data=data,
            json=json,
            params=kwargs,
            allow_redirects=True,
            raise_for_status=True,
        ) as response:
            ret = await response.json()
            return ret
