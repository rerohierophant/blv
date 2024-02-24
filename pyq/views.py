from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .APIs import img_result, pyq_result, free_query
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
from .models import Pyq
from .models import Img
from .models import Comment


def pyqs_init(request):
    pyqs = Pyq.objects.all().prefetch_related('img_set', 'comment_set')
    return render(request, "pyqs.html", {'pyqs': pyqs})


def pyq_detail(request, pyq_id):
    pyq = get_object_or_404(Pyq, pk=pyq_id)  # 根据pyq_id获取Pyq实例
    return render(request, 'pyq_index.html', {'pyq': pyq})


def get_result_all(request):
    data = json.loads(request.body.decode('utf-8'))
    p_id = data.get('id')
    p = Pyq.objects.get(pk=p_id)
    img_urls = list(p.img_set.all().values_list('img_url', flat=True))

    order = "请描述这条朋友圈讲述了什么"

    desc = data.get('desc')

    res = pyq_result(order, img_urls, desc)
    return JsonResponse({'data': res})


def get_result_img(request):
    data = json.loads(request.body.decode('utf-8'))
    img_url = data.get('src')

    order = "请描述这幅图里有什么"

    desc = data.get('desc')

    res = img_result(order, img_url, desc)
    return JsonResponse({'data': res})


def get_free_chat(request):
    data = json.loads(request.body.decode('utf-8'))
    voice_prompt = data.get('voice_input')

    # 从Django的session中获取对话历史
    conversation_history = request.session.get("conversation_history", [])
    conversation_history.append({"type": "text", "text": voice_prompt})

    order = "请根据这条朋友圈的内容回答用户提出的问题"

    desc = data.get('desc')

    p_id = data.get('id')
    p = Pyq.objects.get(pk=p_id)
    img_urls = list(p.img_set.all().values_list('img_url', flat=True))

    res = free_query(order, img_urls, desc, conversation_history)
    return JsonResponse({'data': res})

