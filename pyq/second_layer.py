from .GroundingDINO.groundingdino.util.inference import load_model, load_image, predict, annotate, Model
import cv2
import os
from PIL import Image
import torch
from torchvision.ops import box_convert
import numpy as np

CONFIG_PATH = "pyq/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
CHECKPOINT_PATH = "static/models/groundingdino_swint_ogc.pth"
DEVICE = "cpu"
# IMAGE_PATH = "../static/img/img2.jpg"
BOX_TRESHOLD = 0.35
TEXT_TRESHOLD = 0.25


def get_second_layer(TEXT_PROMPT):
    IMAGE_PATH = "static/dist/assets/data/target.jpg"
    image_source, image = load_image(IMAGE_PATH)
    model = load_model(CONFIG_PATH, CHECKPOINT_PATH)
    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD,
        device=DEVICE,
    )

    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    cv2.imwrite("pyq/annotated_image_t2.jpg", annotated_frame)
    annotated_frame = annotated_frame[..., ::-1]  # BGR to RGB
    image_mask = generate_masks_with_grounding(image_source, boxes)

    # 假设img1和img2已经是PIL Image对象
    img1 = Image.fromarray(image_source)
    img2 = Image.fromarray(image_mask)

    img2_gray = cv2.cvtColor(image_mask, cv2.COLOR_BGR2GRAY)

    # 二值化，将非白色像素转换为黑色，白色保持不变
    # 这里假设白色方框的像素值接近255，可以根据需要调整阈值
    _, binary_mask = cv2.threshold(img2_gray, 240, 255, cv2.THRESH_BINARY)

    # 找到二值化图像中的轮廓
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 如果有多个白色方框，可能需要其他逻辑来选择正确的轮廓
    largest_contour = max(contours, key=cv2.contourArea)

    # 计算轮廓的边界框
    x, y, w, h = cv2.boundingRect(largest_contour)
    print(x)
    # 使用边界框从原图img1中截取对应区域
    cropped_img1 = image_source[y:y + h, x:x + w]

    # 将结果转换回PIL图像，以便显示或进一步处理
    cropped_img1_pil = Image.fromarray(cropped_img1)

    # 显示结果
    # cropped_img1_pil.show()

    # 定义保存图片的路径和文件名
    filename = 'static/dist/assets/data/target_layer.jpg'

    # 使用 cv2.imwrite 保存图片
    cropped_img1_pil.save(filename)
    return x,y,w,h


def generate_masks_with_grounding(image_source, boxes):
    h, w, _ = image_source.shape
    boxes_unnorm = boxes * torch.Tensor([w, h, w, h])
    boxes_xyxy = box_convert(boxes=boxes_unnorm, in_fmt="cxcywh", out_fmt="xyxy").numpy()
    mask = np.zeros_like(image_source)
    for box in boxes_xyxy:
        x0, y0, x1, y1 = box
        mask[int(y0):int(y1), int(x0):int(x1), :] = 255
    return mask
