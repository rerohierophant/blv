from PIL import Image
import base64
from io import BytesIO


def merge_images(base64_str, background_path, output_path):
    # 将base64字符串转换为图片
    image_data = base64.b64decode(base64_str.split(',')[1])  # 移除base64前缀
    image = Image.open(BytesIO(image_data))

    # 加载背景图片
    background = Image.open(background_path).convert("RGBA")

    # 确保两张图片的大小一致
    image = image.resize(background.size)

    # 将图片叠加到背景上
    background.paste(image, (0, 0), image)
    # 将结果图片转换为RGB模式
    result_image = background.convert("RGB")
    # 保存结果图片
    result_image.save(output_path, "JPEG")

    return output_path
