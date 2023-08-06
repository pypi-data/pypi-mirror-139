import dict_tools.data as data

# https://console.cloud.vmware.com/csp/gateway/am/api/swagger-ui.html
PUBLIC_CSP_URL = "https://console.cloud.vmware.com"


async def gather(hub, profiles):
    """
    Given a refresh token, retrieve an access token.
    If a default_org_id isn't supplied, use the default org of the connected account.
    Any extra parameters will be saved as part of the profile.

    Example:

    .. code-block:: yaml

        csp.token:
          profile_name:
            refresh_token: dmd23q3au8ljyajcvhz207of4ivsn9vjiaxzez223qeagdpe0voqiasknykv58jt
            # optional configuration
            csp_url: https://console.cloud.vmware.com
            default_org_id: my_org_id
            my_kwarg: my_value
    """
    sub_profiles = {}
    for profile, ctx in profiles.get("csp.token", {}).items():
        try:
            # Fall back on to the public CSP url
            ctx.csp_url = ctx.get("csp_url", PUBLIC_CSP_URL)
            token = ctx.get("refresh_token") or ctx.get("token")

            hub.log.debug(f"connecting to csp with profile: {profile}")
            token_data = await hub.exec.request.json.post(
                data.NamespaceDict(acct={"headers": {"refresh_token": token}}),
                url=f"{ctx.csp_url}/csp/gateway/am/api/auth/api-tokens/authorize",
                allow_redirects=True,
                raise_for_status=True,
                params={"refresh_token": token},
            )
            if not token_data:
                continue

            ctx.headers = {
                "csp-auth-token": token_data.ret.access_token,
            }

            if "default_org_id" not in ctx:
                loggedin_user_profile = await hub.exec.request.json.get(
                    data.NamespaceDict(acct=ctx),
                    url=f"{ctx.csp_url}/csp/gateway/am/api/loggedin/user/profile",
                    allow_redirects=True,
                    raise_for_status=True,
                )
                if loggedin_user_profile:
                    ctx.default_org_id = loggedin_user_profile.ret.get("defaultOrgId")
                else:
                    ctx.default_org_id = None

            sub_profiles[profile] = ctx
            hub.log.debug(f"connected to csp with profile: {profile}")
        except Exception as e:
            hub.log.error(f"{e.__class__.__name__}: {e}")
            continue

    return sub_profiles
