from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .get_api import result
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import login, logout

# Create your views here.
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
def get_result_all(request):
    data = json.loads(request.body.decode('utf-8'))
    p_id = data.get('id')
    p = Pyq.objects.get(pk=p_id)
    img_url = list(p.img_set.all().values_list('img_url', flat=True))[0]

    order = "请描述这条朋友圈讲述了什么"

    desc = data.get('desc')
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    settings = {
        'description_style': user_profile.description_style,
        'aesthetics': user_profile.aesthetics,
        'emotional': user_profile.emotional,
        'Confidence': user_profile.Confidence,
    }
    res = result(order, img_url, desc, p, settings)
    return JsonResponse({'data': res})

@login_required
def get_result_img(request):
    data = json.loads(request.body.decode('utf-8'))
    img_url = data.get('src')

    order = "请描述这幅图里有什么"

    desc = data.get('desc')

    res = result(order, img_url, desc)
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