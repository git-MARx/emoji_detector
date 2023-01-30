import cv2
import random
import os



out_path = "./dataset/"
images_path = './images/'
emoji_path = './emoji/apple/'
image_count = 5

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

def zoom(img, scale_percent=100):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized


os.makedirs(out_path, exist_ok=True)
for i in range(image_count):
    background = cv2.imread(images_path + random.choice(os.listdir(images_path)))
    overlay = cv2.imread(emoji_path + random.choice(os.listdir(emoji_path)), cv2.IMREAD_UNCHANGED)  # IMREAD_UNCHANGED => open image with the alpha channel
    overlay = rotate(overlay, random.choice([30, 45, 60, 90, 115, 130, 145, 180, 225, 240, 270, 300, 315, 360]))
    resize_constant = random.randint(50, 300) / 100
    overlay = zoom(overlay, resize_constant * 100)
    x_off = random.randrange(0, int(background.shape[1]-(resize_constant*80)))
    y_off = random.randrange(0, int(background.shape[0]-(resize_constant*80)))
    height, width = overlay.shape[:2]

    start_point = (x_off, y_off)

    end_point = (x_off+ int(resize_constant*74), y_off+ int(resize_constant*74))
    # color = (255, 0, 0)
    # # Line thickness of 2 px
    # thickness = 2
    for y in range(height):
        for x in range(width):
            overlay_color = overlay[y, x, :3]  # first three elements are color (RGB)
            overlay_alpha = overlay[y, x, 3] / 255  # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0

            # get the color from the background image
            background_color = background[y+y_off, x+x_off]

            # combine the background color and the overlay color weighted by alpha
            composite_color = background_color * (1 - overlay_alpha) + overlay_color * overlay_alpha
            background[y+y_off, x+x_off] = composite_color
    # background = cv2.rectangle(background, start_point, end_point, color, thickness)
    f = open(out_path + str(i+1) +'.txt', 'w')
    f.write(f'{x_off} {y_off} {x_off+ int(resize_constant*74)} {y_off+ int(resize_constant*74)}')
    f.close()
    cv2.imwrite(out_path + str(i+1) +'.png', background)
