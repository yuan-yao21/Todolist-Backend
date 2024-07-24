import base64
import datetime
import scrypt
import jwt

from django.conf import settings
from django.http import JsonResponse

from user.controllers import get_user


def verify_jwt(token):
    """
    校验jwt
    :param token: jwt
    :return: dict: payload
    """
    secret = settings.JWT_SECRET

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        payload = None

    return payload


def jwt_authentication(request):
    """
    根据jwt验证用户身份
    """
    request.user = None
    auth_header = request.headers.get("Authorization")
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0] == 'Bearer':
            token = parts[1]
            payload = verify_jwt(token)
            if payload:
                user_id = payload.get("user_id")
                user, result = get_user(user_id)
                if result:
                    request.user = user
        else:
            print("Invalid Authorization header format.")


def login_required(func):
    """
    用户必须登录装饰器
    使用方法：放在 method_decorators 中
    """

    # @wraps(func)
    def wrapper(request, *args, **kwargs):
        jwt_authentication(request)
        if not request.user:
            return JsonResponse(
                {"message": "User must be authorized."}, status=401
            )
        else:
            return func(request, *args, **kwargs)

    return wrapper


def encrypt_password(password):
    salt = settings.SALT
    key = scrypt.hash(password, salt, 32768, 8, 1, 32)
    return base64.b64encode(key).decode("ascii")


def generate_jwt(payload, expiry=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :return: 生成jwt
    """
    if expiry is None:
        now = datetime.datetime.now()
        expire_hours = (
            int(settings.JWT_EXPIRE_HOURS)
            if int(settings.JWT_EXPIRE_HOURS) > 0
            else 1
        )
        expiry = now + datetime.timedelta(hours=expire_hours)
        print("now:", now)
        print("expiry:", expiry)

    _payload = {"exp": expiry}
    _payload.update(payload)

    secret = settings.JWT_SECRET

    token = jwt.encode(_payload, secret, algorithm="HS256")

    return token
