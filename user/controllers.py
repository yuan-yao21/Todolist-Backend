from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import User


def get_user(user_id):
    try:
        u = User.objects.get(id=user_id)
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False
    

def create_user(username, password):
    try:
        now=timezone.now()
        u = User.objects.create(
            username=username,
            password=password,
            created=now,
            updated=now
        )
        u.save()
        return True
    except Exception as e:
        print(e)
        return False
    

def update_user(user_id, password, nickname, mobile, bio, head_image):
    try:
        u = User.objects.get(id=user_id)
        u.password = password
        u.nickname = nickname
        u.mobile = mobile
        u.bio = bio
        u.head_image = head_image
        u.updated = timezone.now()
        u.save()
        return True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False


def get_user_with_pass(username, password):
    try:
        u = User.objects.get(username=username)
        if not u.password == password:
            return "not found", False
        return u, True
    except ObjectDoesNotExist:
        return "not found", False
    except Exception as e:
        print(e)
        return "errors", False
    