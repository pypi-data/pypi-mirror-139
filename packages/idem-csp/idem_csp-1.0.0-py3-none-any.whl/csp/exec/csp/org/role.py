__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, org_id: str = None):
    ret = await hub.tool.csp.org.get(ctx, "roles", org_id=org_id, expand=True)
    return ret["orgRolesData"]


async def get(hub, ctx, role_id: str, org_id: str = None):
    return await hub.tool.csp.org.get(ctx, f"roles/{role_id}", org_id=org_id)
