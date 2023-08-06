# -*- coding: utf-8 -*-

"""
This module define all Exceptions for GDetect.
GDetectError is for all external call.
All other exceptions are for internal use.
"""


class GDetectError(BaseException):
    """global error for external return"""


class NoAuthenticateToken(ValueError):
    """no token to authentication exists"""


class BadAuthenticationToken(ValueError):
    """given token has bad format"""


class NoURL(ValueError):
    """no URL to API found"""


class UnauthorizedAccess(ValueError):
    """access to API is unauthorized"""


class BadUUID(ValueError):
    """given UUID is wrong"""


# ReqResp = namedtuple("ReqResp", "response, ok, error, message")


# def req(func):
#     def handle(*args, **kwargs):
#         try:
#             r = func(*args, **kwargs)
#         except requests.ConnectionError as ex:
#             return ReqResp(None, False, ex, "unable to connect")
#         except requests.HTTPError as ex:
#             code = ex.response.status_code
#             msg = status_msg(code)
#             return ReqResp(None, False, ex, msg)
#         except request.URLRequiered as ex:
#             return ReqResp(None, False, ex, "an URL is requiered")
#         except requests.TooManyRedirects as ex:
#             return ReqResp(None, False, ex, "too many redirects")
#         except requests.Timeout as ex:
#             return ReqResp(None, False, ex, "request timed out")
#         except BaseException as ex:
#             return ReqResp(None, False, ex, "undefined error")

#         return ReqResp(r, True, None, "")

#     return handle
