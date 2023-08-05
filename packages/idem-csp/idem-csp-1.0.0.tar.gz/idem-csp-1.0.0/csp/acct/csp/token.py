# https://console.cloud.vmware.com/csp/gateway/am/api/swagger-ui.html
PUBLIC_CSP_URL = "https://console.cloud.vmware.com"


async def gather(hub):
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
    for profile, ctx in hub.acct.PROFILES.get("csp.token", {}).items():
        try:
            # Fall back on to the public CSP url
            ctx["csp_url"] = ctx.get("csp_url", PUBLIC_CSP_URL)

            hub.log.debug(f"connecting to csp with profile: {profile}")
            token_data = await hub.tool.csp.init.post(
                url=ctx["csp_url"],
                ref="auth/api-tokens/authorize",
                refresh_token=ctx["refresh_token"],
            )
            ctx["access_token"] = token_data["access_token"]

            if "default_org_id" not in ctx:
                loggdedin_user_profile = await hub.tool.csp.session.request(
                    method="get",
                    url=ctx["csp_url"],
                    base_path=hub.tool.csp.init.PATH,
                    ref="loggedin/user/profile",
                    headers={
                        "Content-Type": "application/json",
                        "csp-auth-token": ctx["access_token"],
                    },
                )
                ctx["default_org_id"] = loggdedin_user_profile.get("defaultOrgId")

            sub_profiles[profile] = ctx
            hub.log.debug(f"connected to csp with profile: {profile}")
        except Exception as e:
            hub.log.error(f"{e.__class__.__name__}: {e}")
            continue

    return sub_profiles
