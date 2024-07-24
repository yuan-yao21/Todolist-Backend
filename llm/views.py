from django.http import JsonResponse
from django.shortcuts import render
from zhipuai import ZhipuAI

from utils.jwt import login_required

client = ZhipuAI(api_key="ced3417318535caea904e50cc70b4f6f.rFX0tnZn1k1HFItM")

# Create your views here.
@login_required
def llm_request_summarynote(request):
    if request.method == 'POST':
        user_input = request.POST.get('request_text', '')

        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "user", "content": "作为一名TODO_APP的普通用户，请为我的笔记进行摘要"},
                {"role": "assistant", "content": "当然，为了精简您的笔记，请告诉我您需要摘要的笔记的详细内容"},
                {"role": "user", "content": user_input}
            ],
        )

        return JsonResponse({
            'status': 'success',
            'response': ''.join(response.choices[0].message.content)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
