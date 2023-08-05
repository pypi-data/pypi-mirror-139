async def pre(hub, ctx):
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]

    if "acct" not in func_ctx:
        raise ConnectionError("No profile found")

    if "access_token" not in func_ctx.acct:
        raise ConnectionError(f"No access token found")
