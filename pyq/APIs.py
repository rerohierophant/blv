from openai import OpenAI
import os
import base64
import json
from .models import Img
from django.http import HttpResponse


api_key = "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"
max_tokens = 800
# os.environ["http_proxy"] = "http://localhost:33210"
# os.environ["https_proxy"] = "http://localhost:33210"

key_ele_dict = {
    'activities and experiences': '1.Scene: [location, activities, natural landscape, Architecture, weather]\n'
                                  '2.People: [number, actions, gender, appearance, facial expression, interactions '
                                  'between people, clothes]',

    'goodies sharing': '1.Object: [Name, Number, Color, Shape, Texture, Material, Logo, Text]',

    'expression of emotions or opinions': '1.Scene: [location, activities]\n'
                                          '2.People: [Number, Facial expression, Actions]',

    'personal portraits': '1.Scene: [location, activities]\n'
                          '2.People: [Number, Gender, Appearance, Body shape, Hairstyle, Facial expression, Makeup, '
                          'Actions, Clothes]\n '
                          '3.Object: [Name]',

    'interpersonal relationship': '1.Scene: [location, activities]\n'
                                  '2.People: [Number, Gender, Appearance, Hairstyle, Facial expression, Interactions, '
                                  'Actions, Clothes]\n '
                                  '3.Object: [Name. Number]',
    'Artistic Creations': '1.Scene: [location, activities, Natural Landscape, Architecture]\n'
                          '2.People: [Number, Gender, Appearance,, Facial expression, Interactions, Actions]\n'
                          '3.Object: [Name, Number, Color, Shape, Texture, Material]'

}


def pyq_result(order, img_urls, desc):
    client = OpenAI(
        api_key=api_key,
    )

    img_template = [
        {"type": "text", "text": desc},
    ]
    for img_url in img_urls:
        img_message = {
            "type": "image_url",
            "image_url": {"url": img_url},
        }
        img_template.append(img_message)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": order},
            {
                "role": "user",
                "content": img_template
            }
        ],
        model="gpt-4-vision-preview",
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content


def free_query_pyq(order, img_urls, desc, conversation_history):
    client = OpenAI(
        api_key=api_key,
    )

    img_template = [
        {"type": "text", "text": desc},
    ]
    for img_url in img_urls:
        img_message = {
            "type": "image_url",
            "image_url": {"url": img_url},
        }
        img_template.append(img_message)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": order},
            {
                "role": "user",
                "content": img_template
            },
            {
                "role": "user",
                "content": conversation_history
            }
        ],
        model="gpt-4-vision-preview",
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content


def free_query_img(order, img_url, desc, conversation_history):
    client = OpenAI(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": order},
                    {"type": "text", "text": desc},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },

                ],
            },
            {
                "role": "user",
                "content": conversation_history
            }
        ],
        model="gpt-4-vision-preview",
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content


def img_result(img_url, desc, p, settings):
    caption = p.content
    # type = getImageType(img_url, desc, caption)
    # print(type)
    # key_ele = getKeyEle(img_url, desc, caption, type)
    # print(key_ele)
    img_des = getImgDescription(img_url, desc, caption, key_ele, settings)
    return img_des


def getImageType(img_url, desc, caption):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''There are many types of pictures on social media, including goodies sharing, expression of 
    emotions or opinions, activities and experiences, personal portraits, interpersonal relations and artistic 
    creations. Task: Now I upload a image, the caption of the image is '{caption}'. please help me determine 
    what type it is. You only need to answer the type of the image, for example: "activities and experiences" '''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "text", "text": desc},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        model="gpt-4-vision-preview",

    )
    response = chat_completion.choices[0].message.content
    res = ""

    if "activities and experiences" in response:
        res = "activities and experiences"
    if "goodies sharing" in response:
        res = "goodies sharing"
    if "expression of emotions or opinions" in response:
        res = "expression of emotions or opinions"
    if "personal portraits" in response:
        res = "personal portraits"
    if "interpersonal relationship" in response:
        res = "interpersonal relationship"
    if "Artistic Creations" in response:
        res = "Artistic Creations"

    return res


def getKeyEle(img_url, desc, caption, type):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''I provided you with an image about {type} on social media, the The caption of the image is '{caption}' 
In pictures of the {type} type, people will pay more attention to the following key points in the picture: 
{key_ele_dict[type]} Task: The above elements are not all the key points that the author wants to express, so you can 
omit some unimportant elements. You need to combine pictures and text to filter out which of the above elements in 
the picture are the key points that the author wants to express. Note: You only need to give each key element and a 
brief description of the corresponding'''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "text", "text": desc},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        model="gpt-4-vision-preview",

    )
    return chat_completion.choices[0].message.content


def getImgDescription(img_url, desc, caption, key_ele, settings):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''Please follow the instructions below.
Step1:  identity image type.
There are many types of pictures on social media, including goodies sharing, expression of 
emotions or opinions, activities and experiences, personal portraits, interpersonal relations and artistic creations. 
Task: Now I upload a image, the caption of the image is '{caption}'. please help me determine   what type it is. You only need to answer the type of the image, for example: "activities and experiences"

Step2: identity image key elements.
Now you have identitied the type of the image.You should choose different image highlights in the table below according to different types.
'activities and experiences': '1.Scene: [location, activities, natural landscape, Architecture, weather]'
                                  '2.People: [number, actions, gender, appearance, facial expression, interactions '
                                  'between people, clothes]',

'goodies sharing': '1.Object: [Name, Number, Color, Shape, Texture, Material, Logo, Text]',

'expression of emotions or opinions': '1.Scene: [location, activities]'
                                          '2.People: [Number, Facial expression, Actions]',

'personal portraits': '1.Scene: [location, activities]\n'
                          '2.People: [Number, Gender, Appearance, Body shape, Hairstyle, Facial expression, Makeup, '
                          'Actions, Clothes] '
                          '3.Object: [Name]',

'interpersonal relationship': '1.Scene: [location, activities]\n'
                                  '2.People: [Number, Gender, Appearance, Hairstyle, Facial expression, Interactions, '
                                  'Actions, Clothes] '
                                  '3.Object: [Name. Number]',
'Artistic Creations': '1.Scene: [location, activities, Natural Landscape, Architecture]'
                          '2.People: [Number, Gender, Appearance,, Facial expression, Interactions, Actions]'
                          '3.Object: [Name, Number, Color, Shape, Texture, Material]'
The caption of the image is "雪龄+1".The above elements are not all the key points that the author wants to express, so you can 
omit some unimportant elements. You need to combine pictures and text to filter out which of the above elements in the picture are the key points that the author wants to express.

Step3：describe the image
Please play the role of an image describer, describing images for blind people. We provide 1 image, please describe with image captions. 
Instructions:
(1)   You need to describe in detail each key element of the image in step 2: 
(2)   You should briefly describe elements not mentioned in Instruction(1) 
(3)   Please use Chinese to describe.
(4)   If there is a subject, first describe the subject, and then use the subject as a reference to describe the surrounding objects.If there is no subject, describe it directly in order (clockwise or from left to right)
(5)   The description of the image needs to be closely integrated with the caption\n. 
'''

    description_style = ''
    aesthetics = ''
    emotional = ''
    Confidence = ''
    cur_index = 6
    if settings['description_style'] == "1":
        description_style = f'''({cur_index})Assume that you are the author of this post on Moments. Please describe 
        this post in the first person.\n '''
        prompt += description_style
        cur_index += 1

    if settings['aesthetics'] == True:
        aesthetics = f'''({cur_index})If you feel it is necessary to describe aesthetically relevant aspects, 
        please describe them.\n '''
        prompt += aesthetics
        cur_index += 1
    else:
        aesthetics = ''

    if settings['emotional'] == True:
        emotional = f'''({cur_index})Please describe what kind of mood the author wants to express through this post, and how do I 
        need to comment? Please give some suggestions in comments. \n'''
        prompt += emotional
        cur_index += 1
    else:
        emotional = ''

    print(prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "text", "text": desc},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        model="gpt-4-vision-preview",
        temperature=int(settings['Confidence'])

    )
    return chat_completion.choices[0].message.content


def getSecondLayerDes(img_url, type, caption, img, pre_des_text):
    img.sorted_objs = ""
    img.save()
    # 获取图片中的对象
    objects = getImgObjects(img_url, type)
    # 按重要程度排序
    sorted_objects = getSortedObjects(img_url, objects, type, caption)
    img.sorted_objs = sorted_objects
    img.save()
    sorted_objects_arr = json.loads(sorted_objects)
    print(sorted_objects_arr)
    objects_len = len(sorted_objects_arr)
    loc = getObjectLocation(img_url, sorted_objects_arr[0], pre_des_text)
    print(loc)
    return {"loc": loc, "objects_len": objects_len}


def getImgObjects(img_url, type):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''This is a "{type}" type picture in the circle of friends. Please tell me the main objects that make up this image.
       Note: 
       (1)You only need to name the object, not describe it. For example: the male on the left. 
       (2)When naming objects, you need to pay attention that the name should reflect the unique characteristics of the object compared to other objects.
       (3)Finally, all you need to do is give me an array containing all the objects, please provide each object with a string. No need for any extra text'''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        temperature=0.95,
        model="gpt-4-vision-preview",
    )
    response = chat_completion.choices[0].message.content
    return response


def getSortedObjects(img_url, objects, type, caption):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''This is a "{type}" type image. The caption of the image is {caption}. This type of image has the following key points {key_ele_dict[type]}.
You have identified the following objects in this image:
{objects} Please refer to the number of key points that each object has (including the more important points, 
the higher the importance of the object may be), and combine the accompanying text of the image to understand the key 
points that the author wants to express, and sort the importance of each object 
NOTE: all you need to do is give me a sorted array containing all the objects, please provide each object with a string. No need for any extra text'''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        model="gpt-4-vision-preview",
    )
    response = chat_completion.choices[0].message.content
    return response


def getMarkedObjectsDescription(type, caption, ori_img_url, marked_objects):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''This is an "{type}" type image in the circle of friends. The caption of the image is "{caption}".
                 Task: Please describe the "{marked_objects}" in the image
                 Note:Answer me in Chinese'''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": ori_img_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        temperature=1,
        model="gpt-4-vision-preview",
    )
    response = chat_completion.choices[0].message.content
    return response


def getObjectLocation(img_url, obj_name, pre_des_text):
    client = OpenAI(
        api_key=api_key,
    )
    prompt = f'''Suppose you are a person who describes pictures for the blind. Now please identify the [{obj_name}] in the picture and tell the blind person the orientation of this object. Your orientation description needs to include the size and orientation of the object in the image
NOTE: 
(1)You need to identify the complete object.
(2)You just need to tell me the location information of the object, without any extra text,no object description is required
(3)Answer me in Chinese, and start your description with the sentense: "{pre_des_text}"'''

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=max_tokens,
        temperature=0.95,
        model="gpt-4-vision-preview",
    )
    response = chat_completion.choices[0].message.content
    return response



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
