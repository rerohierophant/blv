import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from django.shortcuts import render, get_object_or_404
from .APIs import img_result, pyq_result, free_query_pyq, free_query_img, getSecondLayerDes, getObjectLocation

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login, logout
from django.conf import settings
import requests
from .sam_get_embedding import get_embedding
# from .sam_get_onnx import get_onnx
from .second_layer import explore
from .text2speech import text2speech

from .models import Pyq
from .models import Img
from .models import Comment
import json


@login_required
def pyqs_init(request):
    pyqs = Pyq.objects.all().prefetch_related('img_set', 'comment_set')
    return render(request, "pyqs.html", {'pyqs': pyqs})


@login_required
def pyq_detail(request, pyq_id):
    pyq = get_object_or_404(Pyq, pk=pyq_id)  # 根据pyq_id获取Pyq实例
    return render(request, 'pyq_index.html', {'pyq': pyq})


def pre_loc_info(obj_id):
    pre_text = ""
    if int(obj_id) == 0:
        pre_text = "现在你进入了图像探索模式，现在探索图像中的最主体部分。"
    else:
        pre_text = f"现在探索图像中的第{str(int(obj_id) + 1)}个主体部分。"
    return pre_text


@login_required
def img_detail(request, pyq_id, img_id):
    pyq = get_object_or_404(Pyq, pyq_id=pyq_id)
    img = get_object_or_404(Img, img_id=img_id, pyq=pyq)
    # data = json.loads(request.body.decode('utf-8'))
    # img_id = data.get("img_id")
    # pyq_id = data.get("pyq_id")
    caption = pyq.content
    type = img.type
    img_url = img.img_url
    payload = getSecondLayerDes(img_url, type, caption, img, pre_loc_info(0))
    loc = payload["loc"]
    objects_len = payload["objects_len"]
    audio_fp = f"{text2speech(loc)}"
    # return JsonResponse({'data': loc, 'audio_fp': audio_fp, ' ': objects_len})
    return render(request, 'index.html', {'data': loc, 'audio_fp': audio_fp, 'objects_len': objects_len})
    # return render(request, 'index.html', {'img': img, 'pyq': pyq})


@login_required
def get_result_all(request):
    data = json.loads(request.body.decode('utf-8'))
    p_id = data.get('id')
    p = Pyq.objects.get(pk=p_id)
    img_urls = list(p.img_set.all().values_list('img_url', flat=True))

    order = "请描述这条朋友圈讲述了什么"

    desc = data.get('desc')

    res = pyq_result(order, img_urls, desc)
    audio_fp = text2speech(res)
    return JsonResponse({'data': res, 'audio_fp': audio_fp})


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
    audio_fp = text2speech(res)
    return JsonResponse({'data': res, 'audio_fp': audio_fp})


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
    audio_fp = text2speech(res)
    return JsonResponse({'data': res, 'audio_fp': audio_fp})


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


def delete_specific_file(request):
    file_path_img = 'static/dist/assets/data/target.jpg'
    file_path_embedding = 'static/dist/assets/data/embedding.npy'
    try:
        if os.path.exists(file_path_img):
            os.remove(file_path_img)
            os.remove(file_path_embedding)
            return JsonResponse({"status": "success", "message": "File deleted successfully."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def second_layer_explore(request):
    data = json.loads(request.body.decode('utf-8'))
    img_id = data.get("img_id")
    cur_id = int(data.get("cur_id"))
    img = Img.objects.get(pk=img_id)
    pyq_id = data.get("pyq_id")
    pyq = Pyq.objects.get(pk=pyq_id)
    caption = pyq.content
    type = img.type
    img_url = img.img_url
    sorted_object = img.sorted_objs
    sorted_object_arr = json.loads(sorted_object)
    cur_obj = sorted_object_arr[cur_id]
    loc = getObjectLocation(img_url, cur_obj, pre_loc_info(cur_obj))
    cur_obj_axis = explore_object(cur_obj, img_id)
    audio_fp = f"{text2speech(loc)}"
    return JsonResponse({'loc': loc, 'audio_fp': audio_fp, 'cur_obj_axis': cur_obj_axis})


# TODO 根据图中对象描述获取对象的方法写在这里。输出为矩形框的坐标
def explore_object(obj_name, img_id):
    return ""

