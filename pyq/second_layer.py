import cv2

def explore(rel_pos):
    file_path = 'static/dist/assets/data/target.jpg'
    # 加载本地图片
    image = cv2.imread(file_path)
    # 圆圈的中心坐标
    height, width = image.shape[:2]
    center_coordinates = (int(rel_pos[0] * width), int(rel_pos[1] * height))
    # 圆的半径
    radius = 20
    # 圆的颜色，BGR格式 (0, 0, 255) 表示红色
    color = (0, 0, 255)
    # 圆的线条宽度 -1 表示要画实心圆
    thickness = -1
    # 在图片上绘制圆圈
    cv2.circle(image, center_coordinates, radius, color, thickness)
    # 显示修改后的图片
    # cv2.imshow('Modified Image', image)
    # 保存修改后的图片
    output_path = 'static/dist/assets/output/target.jpg'
    cv2.imwrite(output_path, image)
    return output_path
