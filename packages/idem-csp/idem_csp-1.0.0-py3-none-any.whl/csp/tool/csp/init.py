PATH = "csp/gateway/am/api"


def __func_alias__(hub):
    """
    Create functions on the hub at this location for common request objects
    """
    aliases = {}
    for method in ("delete", "get", "head", "post", "patch"):
        aliases[method] = _get_caller(hub, method=method)

    return aliases


def _get_caller(hub, method):
    async def _request(url: str, ref: str, **kwargs):
        """
        Make a csp request at the given url

        :param url: The csp endpoint url to use
        :param ref: The rest of the url path that follows the "org_id"
        :param kwargs: Any args to pass to the underlying requests library
        :return: The result of the request
        """
        return await hub.tool.csp.session.request(
            method=method,
            url=url,
            base_path=PATH,
            ref=ref,
            headers={"Content-Type": "application/json",},
            **kwargs,
        )

    return _request
