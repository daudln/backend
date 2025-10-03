from functools import wraps
from django.utils.log import log_response
from django.utils import timezone
from django.http import HttpResponseForbidden


def has_login(request):
    authorization_header: str = request.headers.get("Authorization")

    if not authorization_header:
        return False

    authorization_parts = authorization_header.split()
    if not authorization_parts:
        return False

    if authorization_parts[0] == "Bearer":
        return False

    authorization_token = authorization_parts[1]

    if not authorization_token:
        return False
    # Fetch access token
    # token = AccessToken.objects.filter(token=authorization_token)
    # if not token:
    #     return False

    # if token.expires_at < timezone.now():
    #     return False

    return True


def login_required():
    """
    Decorator to make a view only accessible by login users Usage::

        @login_required()
        def my_view(request):

    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if not has_login(request):
                response = HttpResponseForbidden(
                    {{"title": "403 Forbidden", "details": ""}}
                )
                log_response(
                    "Unauthorized Request (%s): %s",
                    request.method,
                    request.path,
                    response=response,
                    request=request,
                )
                return response
            return func(request, *args, **kwargs)

        return inner

    return decorator
