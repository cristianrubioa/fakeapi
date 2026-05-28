from slowapi import Limiter


def _get_real_ip(request) -> str:
    return request.headers.get("CF-Connecting-IP") or request.client.host


limiter = Limiter(key_func=_get_real_ip)
