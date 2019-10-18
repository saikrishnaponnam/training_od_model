import pandas as pd
from PIL import Image
import shutil


def get_catgeory_map(file="training_demo/annotations/list_category_cloth.txt"):
    _categories = []
    with open(file, 'r') as fp:
        _categories = fp.readlines()[1:]
    _categories = [cat.split()[0] for cat in _categories]

    categories = dict()
    for i in range(len(_categories)):
        categories[i + 1] = _categories[i]
    return categories


def get_ctg_img_map(file="training_demo/annotations/list_category_img.txt"):
    img_cat = []
    with open(file, 'r') as fp:
        img_cat = fp.readlines()[2:]

    cat_img = dict()
    for i in range(len(img_cat)):
        img, cat = img_cat[i].split()
        cat = int(cat)
        if cat in cat_img:
            cat_img[cat].append(img)
        else:
            cat_img[cat] = [img]
    return cat_img


def get_img_ctg_map(file="training_demo/annotations/list_category_img.txt"):
    with open(file, 'r') as fp:
        data = fp.readlines()[2:]

    img_ctg = dict()
    for i in range(len(data)):
        img, cat = data[i].split()
        img_ctg[img] = cat
    return img_ctg


def get_img_status(file="training_demo/Eval/list_eval_partition.txt"):
    with open(file, 'r') as fp:
        data = fp.readlines()[2:]

    img_status = dict()
    for line in data:
        img, eval_staus = line.split()
        img_status[img] = eval_staus
    return img_status


def get_train_test_list(file):
    with open(file, 'r') as fp:
        lines = int(fp.readline())
        image_path, evaluation_status = fp.readline().split()

        split = {'train': [], 'test': [], 'val': []}

        for i in range(lines):
            image_path, evaluation_status = fp.readline().split()
            split[evaluation_status].append(image_path)
        return split


def get_annot_csv(file=None):
    file = "training_demo/annotations/list_bbox.txt"
    with open(file, 'r') as fp:
        data = [line.split() for line in fp.readlines()[2:]]
    # print(img_bbox[:5])

    img_bbox = dict()
    for d in data:
        img_bbox[d[0]] = d[1:]
    # print(img_bbox)

    data = []

    ctg_cls_map = get_catgeory_map()
    # print(ctg_cls_map)
    cat_img = get_ctg_img_map()
    # print(cat_img)
    imgs_status = get_img_status()
    print(imgs_status)
    # return

    for key, imgs in sorted(cat_img.items()):
        ctg = ctg_cls_map[key]
        # print(ctg)
        idx = 1
        for img in imgs:
            print("{} --> {}. {} ".format(ctg, idx, img))
            im = Image.open("training_demo/" + img)
            width, height = im.size
            img_data = [ctg + "_{:05d}.jpg".format(idx), width, height, ctg] + img_bbox[img] + [img, imgs_status[img]]
            data.append(img_data)
            idx += 1

    # print(data[:10])

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'original_filename', 'eval_status']
    xml_df = pd.DataFrame(data, columns=column_name)
    return xml_df


if __name__ == '__main__':
    # file = "training_demo/annotations/list_category_cloth.txt"
    # categories = get_catgeories_map(file)
    # print(categories)

    # partition_file = "training_demo/Eval/list_eval_partition.txt"
    # split_list = get_train_test_list(partition_file)
    # print(split_list['train'])

    # get_annot_csv()

    # print(get_img_ctg_map())
    # print(get_ctg_img_map())
    # print(get_img_status())

    # print(get_annot_csv())
    # df = get_annot_csv()
    # print(df)
    # df.to_csv('training_demo/annotations/annotation.csv', index=None)

    df = pd.read_csv("training_demo/annotation.csv")

    # for idx, row in df.iterrows():
    #     # print(row['original_filename'], row['eval_status'], row['filename'])
    #     print(idx)
    #     shutil.copy("training_demo/" + row['original_filename'], "training_demo/images/" + row['eval_status'] + "/" + row['filename'])

    train_df = pd.DataFrame()
    test_df = pd.DataFrame()
    val_df = pd.DataFrame()
    for idx, row in df.iterrows():
        print(idx)
        if row['eval_status'] == 'train':
            train_df = train_df.append(row)
        elif row['eval_status'] == 'test':
            test_df = test_df.append(row)
        else:
            val_df = val_df.append(row)

    print(len(train_df))
    print(len(test_df))
    print(len(val_df))

    train_df.to_csv('training_demo/data/{}.csv'.format("train"), index=None)
    test_df.to_csv('training_demo/data/{}.csv'.format("test"), index=None)
    val_df.to_csv('training_demo/data/{}.csv'.format("val"), index=None)



