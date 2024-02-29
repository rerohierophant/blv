import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from django.shortcuts import render, get_object_or_404
from .APIs import img_result, pyq_result, free_query_pyq, free_query_img
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login, logout
from django.conf import settings
import requests
from .sam_get_embedding import get_embedding
# from .sam_get_onnx import get_onnx

from .models import Pyq
from .models import Img
from .models import Comment


@login_required
def pyqs_init(request):
    pyqs = Pyq.objects.all().prefetch_related('img_set', 'comment_set')
    return render(request, "pyqs.html", {'pyqs': pyqs})


@login_required
def pyq_detail(request, pyq_id):
    pyq = get_object_or_404(Pyq, pk=pyq_id)  # 根据pyq_id获取Pyq实例
    return render(request, 'pyq_index.html', {'pyq': pyq})


@login_required
def img_detail(request, pyq_id, img_id):
    pyq = get_object_or_404(Pyq, pyq_id=pyq_id)
    img = get_object_or_404(Img, img_id=img_id, pyq=pyq)
    return render(request, 'index.html', {'img': img, 'pyq': pyq})


@login_required
def get_result_all(request):
    data = json.loads(request.body.decode('utf-8'))
    p_id = data.get('id')
    p = Pyq.objects.get(pk=p_id)
    img_urls = list(p.img_set.all().values_list('img_url', flat=True))

    order = "请描述这条朋友圈讲述了什么"

    desc = data.get('desc')

    res = pyq_result(order, img_urls, desc)

    return JsonResponse({'data': res})


@login_required
def get_result_img(request):
    data = json.loads(request.body.decode('utf-8'))
    img_url = data.get('src')
    p_id = data.get('id')
    p = Pyq.objects.get(pk=p_id)
    desc = data.get('desc')
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    settings = {
        'description_style': user_profile.description_style,
        'aesthetics': user_profile.aesthetics,
        'emotional': user_profile.emotional,
        'Confidence': user_profile.Confidence,
    }
    res = img_result(img_url, desc, p, settings)

    return JsonResponse({'data': res})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            return redirect('/')  # 重定向到登录后的页面
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        print('开始注册')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('存储')
            user = form.save()
            login(request, user)
            return redirect('/')  # 重定向到注册后的页面
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def setting_view(request):
    if request.method == 'POST':
        print('个性化设置')
        data = json.loads(request.body.decode('utf-8'))
        des_style = data.get('des_style')
        aesthetic = data.get('aesthetic')
        emotion = data.get('emotion')
        confidence = data.get('confidence')

        print(des_style)
        print(aesthetic)
        print(emotion)
        print(confidence)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.description_style = des_style
        user_profile.aesthetics = aesthetic
        user_profile.emotional = emotion
        user_profile.Confidence = confidence
        user_profile.save()

        return JsonResponse({'data': 1})
    else:
        return render(request, 'setting.html')


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

    res = free_query_pyq(order, img_urls, desc, conversation_history)
    return JsonResponse({'data': res})


def get_img_chat(request):
    data = json.loads(request.body.decode('utf-8'))
    voice_prompt = data.get('voice_input')
    conversation_history = request.session.get("conversation_history", [])
    conversation_history.append({"type": "text", "text": voice_prompt})
    order = "请根据这张图片的内容回答用户提出的问题"
    desc = data.get('desc')
    img_url = data.get('img_url')
    res = free_query_img(order, img_url, desc, conversation_history)
    return JsonResponse({'data': res})


def test(request):
    return render(request, 'index.html')


def img_embedding(request):
    data = json.loads(request.body.decode('utf-8'))
    img_url = data.get('img_url')

    get_embedding(img_url)
    return JsonResponse({'data': '模型载入中'})


@csrf_exempt
def save_image(request):
    img_url = request.POST.get('img_url')

    if img_url:
        response = requests.get(img_url)
        if response.status_code == 200:
            # 假设你要保存图片到项目的'saved_images'目录下
            file_path = f'static/dist/assets/data/target.jpg'
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return JsonResponse({'message': '图片保存成功！'}, status=200)
        else:
            return JsonResponse({'error': '无法下载图片'}, status=500)
    else:
        return JsonResponse({'error': '无效的图片ID'}, status=400)

