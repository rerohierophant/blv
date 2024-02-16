from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .get_api import result
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
    img_url = list(p.img_set.all().values_list('img_url', flat=True))[0]

    order = "请描述这条朋友圈讲述了什么"

    desc = data.get('desc')

    res = result(order, img_url, desc)
    return JsonResponse({'data': res})


def get_result_img(request):
    data = json.loads(request.body.decode('utf-8'))
    img_url = data.get('src')

    order = "请描述这幅图里有什么"

    desc = data.get('desc')

    res = result(order, img_url, desc)
    return JsonResponse({'data': res})