# -*- coding: utf-8 -*-


def register_params_check(content: dict):
    # 定义错误信息
    error_messages = {
        'username': "Invalid username",
        'password': "Invalid password",
    }

    # 检查是否缺失字段
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in content:
            return error_messages[field], False

    return "ok", True
