# https://vdc-download.vmware.com/vmwb-repository/dcr-public/7baea724-ebcb-4fba-b604-44cf9fe035ed/6b5f7b84-3be1-4bb3-8894-4e6da76e668e/vrealize-automation-identity-api.json
__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, **kwargs):
    ret = await hub.tool.csp.org.get(ctx, "users", **kwargs)
    return ret["users"]


async def search(hub, ctx, user_search_term: str = "@", **kwargs):
    result = await hub.tool.csp.org.get(
        ctx, f"users/search", userSearchTerm=user_search_term, **kwargs,
    )
    ret = []
    for r in result["results"]:
        user = r.pop("user")
        user.update(r)
        ret.append(user)
    return ret
