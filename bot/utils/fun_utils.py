import cv2
import requests
from utils.basic import *


def download_image(url, filename):
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    else:
        return 'Ошибка при скачивании изображения'


def resize_image_if_small(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Получение размеров изображения
    height, width = image.shape[:2]

    # Проверка, нужно ли изменять размер изображения
    if height < 256 or width < 256:
        # Вычисление коэффициента масштабирования
        scale_factor = max(256 / height, 256 / width)

        # Увеличение изображения
        new_dimensions = (int(width * scale_factor), int(height * scale_factor))
        resized_image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)

        # Сохранение увеличенного изображения
        cv2.imwrite(image_path, resized_image)
        return 'Изображение было увеличено.'
    else:
        return 'Изображение уже достаточно большое.'


def create_tip_image(name_1: str, name_2: str, avatar_path_1: str, avatar_path_2: str, top_left_corner_1: tuple = (107, 56),
                     top_left_corner_2: tuple = (748, 56), center_1: int = 235, center_2: int = 876, text_y: int = 360,
                     template_path: str = 'images/tip_template.png', text_color_1: tuple = (255, 255, 255, 255), text_color_2: tuple = (255, 255, 255),
                     font_scale: int = 1, font_thickness: int = 2, output_path: str = 'temp/tip.png') -> str:
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    # First avatar
    avatar_1 = cv2.imread(avatar_path_1, cv2.IMREAD_UNCHANGED)
    # Проверка наличия альфа-канала в аватаре
    if avatar_1.shape[2] == 4:
        alpha_s = avatar_1[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            template[top_left_corner_1[1]:top_left_corner_1[1] + avatar_1.shape[0], top_left_corner_1[0]:top_left_corner_1[0] + avatar_1.shape[1], c] = \
                (alpha_s * avatar_1[:, :, c] + alpha_l * template[top_left_corner_1[1]:top_left_corner_1[1] + avatar_1.shape[0],
                                                         top_left_corner_1[0]:top_left_corner_1[0] + avatar_1.shape[1], c])
    else:
        # Если альфа-канал отсутствует, копируем только цветовые каналы
        template[top_left_corner_1[1]:top_left_corner_1[1] + avatar_1.shape[0], top_left_corner_1[0]:top_left_corner_1[0] + avatar_1.shape[1],
        :3] = avatar_1

    font = cv2.FONT_HERSHEY_SIMPLEX

    text_size_1 = cv2.getTextSize(name_1, font, font_scale, font_thickness)[0]

    while text_size_1[0] > 350:
        name_1 = name_1[:-4] + "..."
        text_size_1 = cv2.getTextSize(name_1, font, font_scale, font_thickness)[0]
        center_1 += 5
    text_position_1 = (center_1 - (text_size_1[0] // 2), text_y)

    cv2.putText(template, name_1, text_position_1, font, font_scale, text_color_1, font_thickness, lineType=cv2.LINE_AA)

    # Second avatar
    avatar_2 = cv2.imread(avatar_path_2, cv2.IMREAD_UNCHANGED)
    if avatar_2.shape[2] == 4:
        alpha_s = avatar_2[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            template[top_left_corner_2[1]:top_left_corner_2[1] + avatar_2.shape[0], top_left_corner_2[0]:top_left_corner_2[0] + avatar_2.shape[1], c] = \
                (alpha_s * avatar_2[:, :, c] + alpha_l * template[top_left_corner_2[1]:top_left_corner_2[1] + avatar_2.shape[0],
                                                         top_left_corner_2[0]:top_left_corner_2[0] + avatar_2.shape[1], c])
    else:
        # Если альфа-канал отсутствует, копируем только цветовые каналы
        template[top_left_corner_2[1]:top_left_corner_2[1] + avatar_2.shape[0], top_left_corner_2[0]:top_left_corner_2[0] + avatar_2.shape[1],
        :3] = avatar_2

    text_size_2 = cv2.getTextSize(name_2, font, font_scale, font_thickness)[0]

    while text_size_2[0] > 350:
        name_2 = name_2[:-4] + "..."
        text_size_2 = cv2.getTextSize(name_2, font, font_scale, font_thickness)[0]
        center_2 += 5
    text_position_2 = (center_2 - (text_size_2[0] // 2), text_y)

    cv2.putText(template, name_2, text_position_2, font, font_scale, text_color_2, font_thickness, lineType=cv2.LINE_AA)

    cv2.imwrite(output_path, template, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return f'[{get_now()}] Tip image created: {output_path}'
