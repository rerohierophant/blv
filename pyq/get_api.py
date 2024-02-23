from openai import OpenAI

import os

os.environ["http_proxy"] = "http://localhost:33210"
os.environ["https_proxy"] = "http://localhost:33210"

key_ele_dict = {
    'activities and experiences': '1.Scene: [location, activities, natural landscape, Architecture, weather]\n'
                                  '2.People: [number, actions, gender, appearance, facial expression, interactions between people, clothes]',

    'goodies sharing': '1.Object: [Name, Number, Color, Shape, Texture, Material, Logo, Text]',

    'expression of emotions or opinions': '1.Scene: [location, activities]\n'
                                          '2.People: [Number, Facial expression, Actions]',

    'personal portraits': '1.Scene: [location, activities]\n'
                          '2.People: [Number, Gender, Appearance, Body shape, Hairstyle, Facial expression, Makeup, Actions, Clothes]\n'
                          '3.Object: [Name]',

    'interpersonal relationship': '1.Scene: [location, activities]\n'
                                  '2.People: [Number, Gender, Appearance, Hairstyle, Facial expression, Interactions, Actions, Clothes]\n'
                                  '3.Object: [Name. Number]',
    'Artistic Creations': '1.Scene: [location, activities, Natural Landscape, Architecture]\n'
                          '2.People: [Number, Gender, Appearance,, Facial expression, Interactions, Actions]\n'
                          '3.Object: [Name, Number, Color, Shape, Texture, Material]'

}


def result(order, img_url, desc, p):
    # client = OpenAI(
    #     api_key="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",
    # )
    #
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {"type": "text", "text": order},
    #                 {"type": "text", "text": desc},
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {
    #                         "url": img_url,
    #                     },
    #                 },
    #             ],
    #         }
    #     ],
    #     max_tokens=100,
    #     model="gpt-4-vision-preview",
    #
    # )
    caption = p.content
    type = getImageType(img_url, desc, caption)
    print(type)
    key_ele = getKeyEle(img_url, desc, caption, type)
    print(key_ele)
    img_des = getImgDescription(img_url, desc, caption, type, key_ele)
    return img_des

def getImageType(img_url, desc, caption):
    client = OpenAI(
        api_key="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",
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
        max_tokens=300,
        model="gpt-4-vision-preview",

    )
    return chat_completion.choices[0].message.content

def getKeyEle(img_url, desc, caption, type):
    client = OpenAI(
        api_key="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",
    )
    prompt = f'''I provided you with an image about {type} on social media, the The caption of the image is '{caption}' 
In pictures of the {type} type, people will pay more attention to the following key points in the picture: 
{key_ele_dict[type]}
Task: The above elements are not all the key points that the author wants to express, so you can omit some unimportant elements. You need to combine pictures and text to filter out which of the above elements in the picture are the key points that the author wants to express. 
Note: You only need to give each key element and a brief description of the corresponding'''

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
        max_tokens=500,
        model="gpt-4-vision-preview",

    )
    return chat_completion.choices[0].message.content


def getImgDescription(img_url, desc, caption, type, key_ele):
    client = OpenAI(
        api_key="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",
    )
    prompt = f'''Context: I provided you with an image about {type} on social media, the The caption of the image is {caption} 
Task: Please play the role of an image describer, describing images for blind people. We provide 1 image, please describe with image captions. 
Instructions:
(1)   You need to describe in detail each key element of the image below: 
{key_ele}
(2)   You should briefly describe elements not mentioned in Instruction(1) 
(3)   If there is a subject, first describe the subject, and then use the subject as a reference to describe the surrounding objects.If there is no subject, describe it directly in order (clockwise or from left to right)
(4)   The description of the image needs to be closely integrated with the caption. 
(5)   Please describe it in one paragraph in Chinese.'''

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
        max_tokens=500,
        model="gpt-4-vision-preview",

    )
    return chat_completion.choices[0].message.content