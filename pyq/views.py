from django.http import HttpResponse
from django.shortcuts import render
from .get_api import result
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def pyq_init(request):
    return render(request, "pyq_index.html")


def get_result(request):
    if request.method == "POST":
        img_url = request.POST.get('src')
        order = "请描述这幅图关于什么"
        desc = request.POST.get('text')
        res = result(order, img_url, desc)
        return JsonResponse({'data': res})


def get_desc(request):
    data = json.loads(request.body)
    time = data.get('time', '未知时间')
    location = data.get('location', '未知地点')
    comments = data.get('comments', '暂无评论')
    content = data.get('content', '暂无正文')
    # 格式化字符串
    result_string = f"发帖时间为{time}，发帖地点为{location}，发帖得到评论为{comments}，发帖正文为{content}"

    # 返回处理结果
    return JsonResponse({'status': 'success', 'desc': result_string})
