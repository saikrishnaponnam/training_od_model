import shutil
import os
from utils import get_catgeories_map, get_img_cat_map





def move_imgs(imgs, cat):
    idx = 1
    des = "training_demo/images/{}/" + cat + "_{:05d}.jpg"
    srcs = {'train': 'training_demo/images_attr/train/', 'test': 'training_demo/images_attr/test/',
            'val': 'training_demo/images_attr/val/'}
    for img in imgs:
        for img_type, src in srcs.items():
            src = os.path.join(src, img)
            if os.path.exists(src):
                # print(src + " ---> " + des.format(img_type, idx))
                shutil.copy(src, des.format(img_type, idx))
                idx += 1
                break


if __name__ == '__main__':
    cat_map = get_catgeories_map("training_demo/annotations/list_category_cloth.txt")

    img__cat_map_file = 'training_demo/annotations/list_category_img.txt'

    img_cat_map = get_img_cat_map(img__cat_map_file)

    for key, cat in cat_map.items():
        # print(key, cat)
        key = str(key)
        if key not in img_cat_map:
            print(key + " not found")
            continue
        imgs = img_cat_map[str(key)]
        move_imgs(imgs, cat)
        # print(len(imgs) > 99999)
