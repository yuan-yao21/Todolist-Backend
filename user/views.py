import json

from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from user import controllers
from user.models import User
from utils.jwt import encrypt_password, generate_jwt, login_required
from utils.register_params_check import register_params_check
from django.views.decorators.http import require_http_methods

# Create your views here.
@login_required
def update_user(request):
    """
    更新用户信息
    """
    if request.method == "OPTIONS":
        return HttpResponse(status=204)

    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        user = request.user

        # 处理普通字段
        password = request.POST.get("password", user.password)
        nickname = request.POST.get("nickname", user.nickname)
        mobile = request.POST.get("mobile", user.mobile)
        bio = request.POST.get("bio", user.bio)

        # 处理文件上传
        head_image = request.FILES.get("head_image", user.head_image)

        result = controllers.update_user(user.id, password, nickname, mobile, bio, head_image)
        if result:
            return JsonResponse({"message": "ok"}, status=200)
        else:
            return JsonResponse({"message": "Error"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"message": "bad arguments"}, status=400)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)


def register_user(request):
    """
    用户注册
    """
    if request.method != "POST":
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
    try:
        content = json.loads(request.body)

        key, passed = register_params_check(content)
        if not passed:
            return JsonResponse(
                {"message": "Invalid arguments: %s" % (key,)}, status=400
            )
        
        username = content["username"]
        password = content["password"]

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already exists"}, status=409)

        result = controllers.create_user(
            username,
            password,
        )
        if result:
            return JsonResponse({"message": "ok"}, status=200)
        else:
            return JsonResponse({"message": "Error"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"message": "bad arguments"}, status=400)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)


def login(request):
    """
    用户登录
    """
    if request.method == "OPTIONS":
        return HttpResponse(status=204)

    if request.method != "PATCH":
        return JsonResponse({"message": "Method not allowed"}, status=405)

    try:
        content = json.loads(request.body)
        username = content["username"]
        password = content["password"]

        user, result = controllers.get_user_with_pass(
            username=username, password=password
        )
        if result:
            jwt = generate_jwt({"user_id": user.id, "nickname": user.nickname})
            return JsonResponse(
                {
                    "jwt": jwt,
                    "userId": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                }
            )
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({"message": "bad arguments"}, status=400)
    except:
        return JsonResponse({"message": "bad arguments"}, status=400)

@login_required
@require_http_methods(["POST"])
def logout(request):
    """
    用户登出
    """
    return JsonResponse({"message": "Logged out successfully. Please delete your JWT."}, status=200)


@login_required
def get_user_info(request):
    """
    获取当前登录用户信息
    """
    user = request.user
    if user.head_image:
        image_url = user.head_image.url
    else:
        image_url = None

    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "mobile": user.mobile,
        "bio": user.bio,
        "head_image": image_url,
        "created": user.created.strftime('%Y-%m-%d %H:%M:%S'),
    })


@login_required
def get_user_info_by_id(request, userId):
    """
    获取指定用户信息
    """
    try:
        user, result = controllers.get_user(userId)
        if result:
            return JsonResponse(
                {
                    "id": user.id,
                    "nickname": user.nickname,
                    "created": user.created,
                }
            )
        else:
            return JsonResponse({"message": user}, status=500)
    except Model.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)
