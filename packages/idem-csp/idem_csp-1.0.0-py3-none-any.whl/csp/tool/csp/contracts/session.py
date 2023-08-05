from typing import Any, Dict


def _sanitize_params(**kwargs) -> Dict[str, Any]:
    ret = {}
    for k, v in kwargs.items():
        if v is None:
            continue
        elif isinstance(v, bool):
            ret[k] = str(v).lower()
        elif isinstance(v, dict):
            ret[k] = _sanitize_params(**v)
        else:
            ret[k] = v
    return ret


async def pre_request(hub, ctx):
    kwargs = ctx.get_arguments()
    request_params = kwargs.get("kwargs", {})
    clean_params = _sanitize_params(**request_params)
    ctx.kwargs.update(clean_params)


async def call_request(hub, ctx):
    try:
        return await ctx.func(*ctx.args, **ctx.kwargs)
    except Exception as e:
        hub.log.error(f"{e.__class__.__name__}: {e}")
        raise


def post_request(hub, ctx):
    if isinstance(ctx.ret, Dict):
        if "results" in ctx.ret:
            return ctx.ret["results"]
    return ctx.ret
